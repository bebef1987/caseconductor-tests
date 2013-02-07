#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest
from pages.home_page import MozTrapHomePage
from pages.run_tests_page import MozTrapRunTestsPage
from pages.manage_runs_page import MozTrapManageRunsPage


class TestRunTestsPage(BaseTest):

    @pytest.mark.moztrap([205, 208])
    def test_that_user_can_pass_test(self, mozwebqa_logged_in):
        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in)

        Assert.false(run_tests_pg.is_test_passed(case_name=case['name']))

        run_tests_pg.pass_test(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_passed(case_name=case['name']))

        self.delete_product(mozwebqa_logged_in, product=case['product'])
        self.delete_profile(mozwebqa_logged_in, profile=case['profile'])

    @pytest.mark.moztrap(206)
    def test_that_user_can_fail_test(self, mozwebqa_logged_in):
        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in)

        Assert.false(run_tests_pg.is_test_failed(case_name=case['name']))

        run_tests_pg.fail_test(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_failed(case_name=case['name']))

        self.delete_product(mozwebqa_logged_in, product=case['product'])
        self.delete_profile(mozwebqa_logged_in, profile=case['profile'])

    @pytest.mark.moztrap(207)
    def test_that_user_can_mark_test_invalid(self, mozwebqa_logged_in):
        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in)

        Assert.false(run_tests_pg.is_test_invalid(case_name=case['name']))

        run_tests_pg.mark_test_invalid(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_invalid(case_name=case['name']))

        self.delete_product(mozwebqa_logged_in, product=case['product'])
        self.delete_profile(mozwebqa_logged_in, profile=case['profile'])

    @pytest.mark.moztrap(2744)
    def test_that_test_run_saves_right_order_of_test_cases(self, mozwebqa_logged_in):
        #get profile, product and version
        profile = self.create_profile(mozwebqa_logged_in)
        product = self.create_product(mozwebqa_logged_in, profile['name'])
        version = product['version']
        #create several test case via bulk create
        cases = self.create_bulk_cases(mozwebqa_logged_in, cases_amount=5, product=product, name='is')
        #create first test suite
        suite_a_cases = (cases[3]['name'], cases[1]['name'])
        suite_a = self.create_suite(
            mozwebqa_logged_in, product=product, name='suite A', case_name_list=suite_a_cases)
        #create second test suite
        suite_b_cases = (cases[2]['name'], cases[0]['name'], cases[4]['name'])
        suite_b = self.create_suite(
            mozwebqa_logged_in, product=product, name='suite B', case_name_list=suite_b_cases)
        #create first test run (suite a, suite b)
        first_suite_order = (suite_a['name'], suite_b['name'])
        first_run = self.create_run(
            mozwebqa_logged_in, activate=True, product=product,
            version=version, suite_name_list=first_suite_order)
        #execute first test run
        home_page = MozTrapHomePage(mozwebqa_logged_in)
        home_page.go_to_home_page()
        home_page.go_to_run_test(
            product_name=product['name'], version_name=version['name'], run_name=first_run['name'],
            env_category=profile['category'], env_element=profile['element'])

        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)
        actual_order = [(item.name, item.suite_name) for item in run_tests_pg.test_items]

        expected_order = [(case, suite) for case in suite_a_cases for suite in (suite_a['name'],)] + \
                        [(case, suite) for case in suite_b_cases for suite in (suite_b['name'],)]
        #assert that right order saved
        Assert.equal(actual_order, expected_order)
        #edit run to reorder suites
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()
        #push run into draft mode
        manage_runs_pg.filter_form.filter_by(lookup='name', value=first_run['name'])
        manage_runs_pg.make_run_draft(first_run['name'])
        #go to edit run page and reorder suites by name (suite b, suite a)
        edit_run_pg = manage_runs_pg.go_to_edit_run_page(first_run['name'])
        second_run = edit_run_pg.edit_run(first_run, reorder_suites=True)
        #make run active again
        manage_runs_pg.filter_form.filter_by(lookup='name', value=first_run['name'])
        manage_runs_pg.activate_run(first_run['name'])
        #execute run again
        home_page.go_to_home_page()
        home_page.go_to_run_test(
            product_name=product['name'], version_name=version['name'], run_name=first_run['name'],
            env_category=profile['category'], env_element=profile['element'])
        #check actual order of items on run tests page
        actual_order = [(item.name, item.suite_name) for item in run_tests_pg.test_items]

        expected_order = [(case, suite) for case in suite_b_cases for suite in (suite_b['name'],)] + \
                        [(case, suite) for case in suite_a_cases for suite in (suite_a['name'],)]
        #assert that right order saved
        Assert.equal(actual_order, expected_order)
