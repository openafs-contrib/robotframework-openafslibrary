Variables
=========

The following environment variables are used to in the OpenAFSLibrary. These
can be used to customize the keywords for your test setup.

When running locally (Library import), the variables may be specified using
Robot Framework test variables.

.. list-table:: Test cell variables
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - AFS_CELL
     - Test cell name
     - ``example.com``
   * - KRB_REALM
     - Authentication realm
     - ``EXAMPLE.COM``
   * - KRB_AFS_KEYTAB
     - Authenication keytab
     - ``robot.keytab``
   * - AKLOG
     - ``aklog`` command path
     - ``aklog``
   * - BOS
     - ``bos`` command path
     - ``bos``
   * - FS
     - ``fs`` command path
     - ``fs``
   * - PAGSH
     - ``pagsh`` commmand path
     - ``pagsh``
   * - PTS
     - ``pts`` command path
     - ``pts``
   * - RXDEBUG
     - ``rxdebug`` command path
     - ``rxdebug``
   * - TOKENS
     - ``tokens`` command path
     - ``tokens``
   * - UDEBUG
     - ``udebug`` command path
     - ``udebug``
   * - UNLOG
     - ``unlog`` command path
     - ``unlog``
   * - VOS
     - ``vos`` command path
     - ``vos``
