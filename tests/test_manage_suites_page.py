#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_suites_page import MozTrapManageSuitesPage


class TestManageSuitesPage(BaseTest):

    def test_that_user_can_create_and_delete_suite(self, mozwebqa_logged_in):
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)

        suite = self.create_suite(mozwebqa_logged_in)

        manage_suites_pg.filter_suites_by_name(name=suite['name'])

        Assert.true(manage_suites_pg.is_element_present(*suite['locator']))

        manage_suites_pg.delete_suite(name=suite['name'])

        Assert.false(manage_suites_pg.is_element_present(*suite['locator']))

        self.delete_product(mozwebqa_logged_in, product=suite['product'])

    def test_that_user_can_create_and_add_cases_to_a_suite(self, mozwebqa_logged_in):
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)
        # create 3 cases
        cases = [self.create_case(mozwebqa=mozwebqa_logged_in, product=product) for i in range(3)]

        # add the first case in the suite
        suite = self.create_suite(mozwebqa=mozwebqa_logged_in, product=product, case_name_list=[case['name'] for case in cases[:1]])

        manage_suites_pg.filter_suites_by_name(name=suite['name'])

        # check that the suite was created
        Assert.true(manage_suites_pg.is_element_present(*suite['locator']))

        manage_test_cases_pg = manage_suites_pg.view_cases(name=suite['name'])

        # check that the first case is in the suite
        for case in cases[:1]:
            Assert.true(manage_test_cases_pg.is_element_present(*case['locator']))

        # open and filter the suite under test
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)
        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_suites_by_name(name=suite['name'])

        edit_suite = manage_suites_pg.edit_suite(name=suite['name'])

        # add the last 2 cases
        edit_suite.add_cases(case['name'] for case in cases[1:])
        edit_suite.save_suite()

        manage_suites_pg.filter_suites_by_name(name=suite['name'])

        # check that the suite was created
        Assert.true(manage_suites_pg.is_element_present(*suite['locator']))

        manage_test_cases_pg = manage_suites_pg.view_cases(name=suite['name'])

        # check that the first 5 cases are in the suite
        for case in cases:
            Assert.true(manage_test_cases_pg.is_element_present(*case['locator']), '%s not found in %s' %(case['name'], suite['name']))
