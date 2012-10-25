#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.base_page import MozTrapBasePage


class MozTrapEditSuitePage(MozTrapBasePage):

    _page_title = 'MozTrap'
    _include_selected_cases_locator = (By.CSS_SELECTOR, '#suite-edit-form .multiselect .include-exclude .action-include')

    _submit_locator = (By.CSS_SELECTOR, '#suite-edit-form .form-actions button[type="submit"]')

    def add_cases(self, case_list):
        for case in case_list:
            case_element = self.selenium.find_element(By.XPATH, "//article[@data-title='%s']/input" % case)
            case_element.click()
        self.selenium.find_element(*self._include_selected_cases_locator).click()

    def save_suite(self):
        self.selenium.find_element(*self._submit_locator).click()
