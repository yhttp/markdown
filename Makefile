PKG_NAMESPACE = yhttp.markdown
PKG_NAME = yhttp-markdown
VENV_NAME = yhttp
PYTEST_FLAGS = -vv
PYDEPS_COMMON = \
	'coveralls' \
	'bddrest >= 6.3.3, < 7' \
	'bddcli >= 2.10.1, < 3' \
	'pytest-fixkit >= 1.1.1' \
	'requests'


# Assert the python-makelib version
PYTHON_MAKELIB_VERSION_REQUIRED = 4


# Ensure the python-makelib is installed
PYTHON_MAKELIB_PATH = /usr/local/lib/python-makelib
ifeq ("", "$(wildcard $(PYTHON_MAKELIB_PATH))")
  MAKELIB_URL = https://github.com/pylover/python-makelib
  $(error python-makelib is not installed. see "$(MAKELIB_URL)")
endif


# Include a proper bundle rule file.
include $(PYTHON_MAKELIB_PATH)/venv-lint-test-webapi.mk


YHTTP_FLAGS = \
	-Odebug=True \
	-Cexamples


serve:
	$(PREFIX)/bin/yhttp-markdown $(YHTTP_FLAGS) serve
