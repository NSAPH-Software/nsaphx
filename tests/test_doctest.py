
import doctest
import unittest

import nsaphx.database as database
#import nsaphx.gps as gps
#import nsaphx.project_controller as project_controller


def test_doctest_suit():
    test_suit = unittest.TestSuite()

    # add tests
    #test_suit.addTest(doctest.DocTestSuite(gps))
    # test_suit.addTest(doctest.DocTestSuite(gps_utils))
    test_suit.addTest(doctest.DocTestSuite(database))
    #test_suit.addTest(doctest.DocTestSuite(project_controller))
    
    # set runner
    runner = unittest.TextTestRunner(verbosity=2).run(test_suit)

    assert not runner.failures