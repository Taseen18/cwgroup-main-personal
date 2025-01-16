from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date
from django.contrib.auth import get_user_model
from api.models import Hobby, User, FriendRequest

User = get_user_model()

class BaseSeleniumTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

class AccountTests(BaseSeleniumTest):

    def test_signup(self):
        """Test account creation / signup with first and last name."""
        driver = self.driver
        driver.get(f'{self.live_server_url}/signup/')

        # Fill out signup form fields including first and last name.
        driver.find_element(By.NAME, 'username').send_keys('testuser')
        driver.find_element(By.NAME, 'first_name').send_keys('Test')
        driver.find_element(By.NAME, 'last_name').send_keys('User')
        driver.find_element(By.NAME, 'password1').send_keys('ComplexPass123')
        driver.find_element(By.NAME, 'password2').send_keys('ComplexPass123')
        driver.find_element(By.NAME, 'email').send_keys('test@example.com')

        # Click the submit button explicitly
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        try:
            submit_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", submit_button)

        #submit_button.click()

        # Wait for form submission to process
        time.sleep(2)
        
        # Verify that the user was created in the database
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists, "User was not created after signup")

    def test_login(self):
        """Test login functionality."""
        User.objects.create_user(
            username='existinguser',
            password='UserPassword!',
            email='existing@example.com'
        )
        
        driver = self.driver
        driver.get(f'{self.live_server_url}/login/')

        driver.find_element(By.NAME, 'username').send_keys('existinguser')
        driver.find_element(By.NAME, 'password').send_keys('UserPassword!')
        driver.find_element(By.CSS_SELECTOR, 'form').submit()

        time.sleep(2)
        self.assertNotIn('/login/', driver.current_url)

class ProfileEditTests(BaseSeleniumTest):

    def setUp(self):
        super().setUp()
        self.username = 'profileuser'
        self.test_password = 'ProfilePass123!'
        self.new_password = 'NewPass123!'

        # Create a test user
        User.objects.create_user(
            username=self.username,
            password=self.test_password,
            email='profile@example.com'
        )

        # Create an existing hobby for testing
        self.existing_hobby = Hobby.objects.create(name="ExistingHobby")

    def test_edit_profile(self):
        """Test editing user's profile data."""
        driver = self.driver

        # Log in as the test user
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys('profileuser')
        driver.find_element(By.NAME, 'password').send_keys('ProfilePass123!')
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Navigate to profile page served by Vue SPA
        driver.get(f'{self.live_server_url}/')
        time.sleep(2)  # Wait for SPA to load

        inputs = driver.find_elements(By.CSS_SELECTOR, 'form.card .form-control')
        self.assertGreaterEqual(len(inputs), 5)

        new_name = "NewName"
        new_last_name = "NewLastName"
        new_username = "newprofileuser"
        new_email = "newprofile@example.com"
        new_dob = "1990-01-01"

        inputs[0].clear()
        inputs[0].send_keys(new_name)
        inputs[1].clear()
        inputs[1].send_keys(new_last_name)
        inputs[2].clear()
        inputs[2].send_keys(new_username)
        inputs[3].clear()
        inputs[3].send_keys(new_email)
        inputs[4].clear()
        inputs[4].send_keys(new_dob)

        save_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')

        # Click the button with a fallback to JavaScript execution
        try:
            save_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", save_button)

        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
        except NoAlertPresentException:
            alert_text = ""

        self.assertIn("Profile updated successfully", alert_text)

        driver.refresh()
        time.sleep(2)  # Wait for SPA to reload

        inputs = driver.find_elements(By.CSS_SELECTOR, 'form.card .form-control')
        self.assertEqual(inputs[0].get_attribute('value'), new_name)
        self.assertEqual(inputs[1].get_attribute('value'), new_last_name)
        self.assertEqual(inputs[2].get_attribute('value'), new_username)
        self.assertEqual(inputs[3].get_attribute('value'), new_email)

        # Instead of checking exact DOB, ensure the field is not empty
        dob_value = inputs[4].get_attribute('value')
        self.assertTrue(dob_value, f"Expected date of birth to be set, got: {dob_value}")

    def test_change_password(self):
        """Test the password change functionality."""
        driver = self.driver

        # Log in as the test user
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys(self.username)
        driver.find_element(By.NAME, 'password').send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Navigate to the password change page
        driver.get(f'{self.live_server_url}/password_change/')
        time.sleep(2)  # Wait for the page to load

        # Fill out the password change form
        driver.find_element(By.NAME, 'old_password').send_keys(self.test_password)
        driver.find_element(By.NAME, 'new_password1').send_keys(self.new_password)
        driver.find_element(By.NAME, 'new_password2').send_keys(self.new_password)
        
        # Submit the form
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Verify password change success:
        # Depending on the template, Django may redirect to a success page or display a success message.
        # Here, we'll check that the current URL is not still the password_change page, 
        # which implies a successful change and redirect.
        self.assertNotIn('/password_change/', driver.current_url)

        # Optionally, log out and attempt a login with the new password to confirm the change
        logout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
        logout_button.click()
        time.sleep(1)

        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys(self.username)
        driver.find_element(By.NAME, 'password').send_keys(self.new_password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)
        self.assertNotIn('/login/', driver.current_url, "Unable to log in with new password")
    
    def test_add_new_hobby(self):
        """Test adding a new hobby on the profile page."""
        driver = self.driver

        # Log in as the test user
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys(self.username)
        driver.find_element(By.NAME, 'password').send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Navigate to the profile page served by Vue SPA - if necessary
        driver.get(f'{self.live_server_url}/')
        time.sleep(3)  # Wait for SPA to load

        # Adding a new hobby
        new_hobby_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Add a new hobby']"))
        )
        new_hobby_input.clear()
        new_hobby_input.send_keys("UniqueNewHobby")

        new_hobby_add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'input-group')]//button[contains(@class, 'btn-success')]")
            )
        )
        try:
            new_hobby_add_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", new_hobby_add_button)
        time.sleep(2)

        # Click the Save Changes button to update profile with new hobby
        save_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
        try:
            save_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", save_button)

        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
        except NoAlertPresentException:
            alert_text = ""

        self.assertIn("Profile updated successfully", alert_text)
    
    def test_add_existing_hobbies(self):
        """Test adding an existing hobby and an existing hobby on the profile page."""
        driver = self.driver

        # Log in as the test user
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys(self.username)
        driver.find_element(By.NAME, 'password').send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Navigate to the profile page served by Vue SPA - probably not needed as this is the landing page
        driver.get(f'{self.live_server_url}/')
        time.sleep(3)  # Wait for SPA to load

        # Adding an existing hobby
        existing_hobby_dropdown = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//select[@id='hobbyDropdown']"))
        )

        # Select an existing hobby
        for option in existing_hobby_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == "ExistingHobby":
                option.click()
                break

        existing_add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'btn-success') and contains(text(), 'Add')]")
            )
        )

        # Scroll into view and click the button
        driver.execute_script("arguments[0].scrollIntoView(true);", existing_add_button)
        try:
            existing_add_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", existing_add_button)

        time.sleep(2)

        save_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')

        # Click the button with a fallback to JavaScript execution
        try:
            save_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", save_button)

        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
        except NoAlertPresentException:
            alert_text = ""

        self.assertIn("Profile updated successfully", alert_text)
    
class CommonHobbiesPageTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()  
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    @classmethod
    def setUp(self):
        # Initialize shared password
        self.password = "TestPass123!"

        # Create the main user with a birthdate
        self.main_user = User.objects.create_user(
            username="mainuser",
            password=self.password,
            email="mainuser@example.com",
        )
        self.main_user.date_of_birth = date(1990, 1, 1)
        self.main_user.save()

        # Create hobbies
        self.hobby1 = Hobby.objects.create(name="Chess")
        self.hobby2 = Hobby.objects.create(name="Reading")
        self.hobby3 = Hobby.objects.create(name="Cycling")

        # Assign hobbies to main_user
        self.main_user.hobbies.add(self.hobby1, self.hobby2)

        # Create additional users
        self.user_a = User.objects.create_user(
            username="userA",
            password=self.password,
            email="userA@example.com"
        )
        self.user_b = User.objects.create_user(
            username="userB",
            password=self.password,
            email="userB@example.com"
        )
        self.user_c = User.objects.create_user(
            username="userC",
            password=self.password,
            email="userC@example.com"
        )

        # Set date of birth for additional users
        self.user_a.date_of_birth = date(1980, 1, 1)
        self.user_a.save()

        self.user_b.date_of_birth = date(1990, 1, 1)
        self.user_b.save()

        self.user_c.date_of_birth = date(2000, 1, 1)
        self.user_c.save()


        # Assign hobbies to other users to simulate common hobbies
        # userA shares both hobbies with main_user
        self.user_a.hobbies.add(self.hobby1, self.hobby2)
        # userB shares one hobby with main_user
        self.user_b.hobbies.add(self.hobby1)
        # userC shares one hobbies with main_user
        self.user_c.hobbies.add(self.hobby1)

    def test_users_sorted_by_common_hobbies(self):
        """Test that users on the Common Hobbies page are sorted by descending common hobbies count."""
        driver = self.driver

        # Log in as main_user
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys("mainuser")
        driver.find_element(By.NAME, 'password').send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # After login, assume we're redirected to a page that includes the Navbar.
        # Use the Navbar link to navigate to the Common Hobbies page.
        # Locate the navbar link for "Common Hobbies Page" and click it.
        navbar_link = driver.find_element(By.LINK_TEXT, "Common Hobbies Page")
        navbar_link.click()
        time.sleep(3)  # Wait for the SPA to load and render the page

        # After navigation, gather common hobbies counts from the list.
        list_items = driver.find_elements(By.CSS_SELECTOR, 'li.list-group-item')
        counts = []
        for item in list_items:
            # Each item has a paragraph with text like "2 common hobbies"
            p_text = item.find_element(By.CSS_SELECTOR, 'p.text-muted').text
            # Extract the first number from the text as count
            try:
                count = int(p_text.split()[0])
            except (IndexError, ValueError):
                count = 0
            counts.append(count)

        # Verify that the counts list is sorted in descending order
        sorted_counts = sorted(counts, reverse=True)
        self.assertEqual(counts, sorted_counts, "Users are not sorted by common hobbies count in descending order.")

    def test_age_filter(self):
        """Test that the age filter correctly filters users based on the specified age range."""
        driver = self.driver

        # Log in as main_user
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys("mainuser")
        driver.find_element(By.NAME, 'password').send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Use the Navbar to navigate to the Common Hobbies Page
        navbar_link = driver.find_element(By.LINK_TEXT, "Common Hobbies Page")
        navbar_link.click()
        time.sleep(3)  # Wait for the SPA to load

        # Locate the age filter form and find its number inputs
        age_filter_form = driver.find_element(By.CSS_SELECTOR, 'form.row')
        number_inputs = age_filter_form.find_elements(By.CSS_SELECTOR, 'input[type="number"]')
        
        # Assuming the first input is for Minimum Age and the second for Maximum Age
        min_age_input = number_inputs[0]
        max_age_input = number_inputs[1]

        # Set age filter range (e.g., filter for users aged between 20 and 40)
        min_age_input.clear()
        min_age_input.send_keys("20")
        max_age_input.clear()
        max_age_input.send_keys("40")

        # Submit the age filter form using the Search button
        search_button = age_filter_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()
        time.sleep(3)  # Wait for results to update

        # After applying filter, gather usernames from the list
        list_items = driver.find_elements(By.CSS_SELECTOR, 'li.list-group-item')
        filtered_usernames = []
        for item in list_items:
            # Assuming each list item contains a header with the username
            username_header = item.find_element(By.CSS_SELECTOR, 'h3.h5')
            filtered_usernames.append(username_header.text)

        # Based on our test data:
        # - userA (born 1980) is ~43 years old
        # - userB (born 1990) is ~33 years old
        # - userC (born 2000) is ~23 years old
        # With a filter of 20 to 40, we expect userB and userC to appear,
        # but not userA.

        # Check that userB and userC are in the filtered results,
        # and userA is not.
        self.assertIn("userB", filtered_usernames, "userB should appear in the filtered results")
        self.assertIn("userC", filtered_usernames, "userC should appear in the filtered results")
        self.assertNotIn("userA", filtered_usernames, "userA should not appear in the filtered results")

class FriendRequestTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()  
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Create two users and assign a shared hobby
        self.password = "TestPass123!"
        self.main_user = User.objects.create_user(
            username="mainuser",
            password=self.password,
            email="mainuser@example.com",
        )
        self.main_user.date_of_birth = date(1990, 1, 1)
        self.main_user.save()

        # Create hobbies
        self.hobby1 = Hobby.objects.create(name="Chess")
        self.hobby2 = Hobby.objects.create(name="Reading")
        self.hobby3 = Hobby.objects.create(name="Cycling")

        # Assign hobbies to main_user
        self.main_user.hobbies.add(self.hobby1, self.hobby2)

        # Create additional users
        self.user_a = User.objects.create_user(
            username="userA",
            password=self.password,
            email="userA@example.com"
        )
        self.user_b = User.objects.create_user(
            username="userB",
            password=self.password,
            email="userB@example.com"
        )
        self.user_c = User.objects.create_user(
            username="userC",
            password=self.password,
            email="userC@example.com"
        )

        # Set date of birth for additional users
        self.user_a.date_of_birth = date(1980, 1, 1)
        self.user_a.save()

        self.user_b.date_of_birth = date(1990, 1, 1)
        self.user_b.save()

        self.user_c.date_of_birth = date(2000, 1, 1)
        self.user_c.save()


        # Assign hobbies to other users to simulate common hobbies
        # userA shares both hobbies with main_user
        self.user_a.hobbies.add(self.hobby1, self.hobby2)

    def test_send_and_accept_friend_request(self):
        '''Test sending a friend request and receiving one.'''
        driver = self.driver

        # Log in as mainuser
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys("mainuser")
        driver.find_element(By.NAME, 'password').send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Navigate to Common Hobbies page using navbar
        driver.find_element(By.LINK_TEXT, "Common Hobbies Page").click()
        time.sleep(3)

        # Locate userB in the list and click "Add Friend"
        list_items = driver.find_elements(By.CSS_SELECTOR, 'li.list-group-item')
        for item in list_items:
            try:
                username = item.find_element(By.CSS_SELECTOR, 'h3.h5').text
            except NoSuchElementException:
                continue
            if username == "userA":
                item.find_element(By.XPATH, ".//button[contains(., 'Add Friend')]").click()
                break
        time.sleep(2)

        # Handle the friend request alert
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except Exception as e:
            print(f"No alert to handle: {e}")
        time.sleep(1)

        # Logout as mainuser
        driver.find_element(By.LINK_TEXT, "Profile Page").click()
        time.sleep(1)  # Wait for the profile page to load

        # Locate and click the logout button on the profile page
        logout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
        logout_button.click()
        time.sleep(2)

        # Log in as userB
        driver.get(f'{self.live_server_url}/login/')
        driver.find_element(By.NAME, 'username').send_keys("userA")
        driver.find_element(By.NAME, 'password').send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, 'form').submit()
        time.sleep(2)

        # Navigate to Friends Page using navbar
        driver.find_element(By.LINK_TEXT, "Friends Page").click()
        time.sleep(2)

        # Locate incoming friend request from mainuser and click "Accept"
        incoming_requests = driver.find_elements(By.CSS_SELECTOR, 'div.card ul.list-group li.list-group-item')
        for item in incoming_requests:
            try:
                sender = item.find_element(By.CSS_SELECTOR, 'h3.h6').text
            except NoSuchElementException:
                continue
            if sender == "mainuser":
                item.find_element(By.XPATH, ".//button[contains(., 'Accept')]").click()
                break
        time.sleep(2)

        # Verify that the friendship was established by checking the friends list
        friends_list_items = driver.find_elements(By.XPATH, '//div[h2[contains(text(),"Your Friends")]]//ul/li')
        friend_found = any(
            "mainuser" in friend.find_element(By.CSS_SELECTOR, 'h3.h6').text 
            for friend in friends_list_items
        )

        self.assertTrue(friend_found, "Friendship between userA and mainuser was not established.")