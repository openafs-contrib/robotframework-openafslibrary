Keywords
========

Access Control List Contains
----------------------------
Fails if an ACL does not contain the given rights.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - name
     - required
     - 
   * - rights
     - required
     - 

Access Control List Matches
---------------------------
Fails if an ACL does not match the given ACL.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - acls
     - 
     - 

Access Control Should Exist
---------------------------
Fails if the access control does not exist for the the given user or group name.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - name
     - required
     - 

Access Control Should Not Exist
-------------------------------
Fails if the access control exists for the the given user or group name.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - name
     - required
     - 

Add Access Rights
-----------------
Add access rights to a path.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - name
     - required
     - 
   * - rights
     - required
     - 

Command Should Fail
-------------------
Fails if command exits with a zero status code.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - cmd
     - required
     - 

Command Should Succeed
----------------------
Fails if command does not exit with a zero status code.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - cmd
     - required
     - 
   * - msg
     - 
     - None

Create Dump
-----------


.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - filename
     - required
     - 
   * - size
     - 
     - small
   * - contains
     - 
     - 

Create Files
------------
Create a directory tree of test files.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - count
     - 
     - 1
   * - size
     - 
     - 0
   * - depth
     - 
     - 0
   * - width
     - 
     - 0
   * - fill
     - 
     - zero

Create Volume
-------------
Create and mount a volume.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name
     - required
     - 
   * - server
     - 
     - None
   * - part
     - 
     - a
   * - path
     - 
     - None
   * - quota
     - 
     - 0
   * - ro
     - 
     - False
   * - acl
     - 
     - None
   * - orphan
     - 
     - False

Directory Entry Should Exist
----------------------------
Fails if directory entry does not exist in the given path.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

File Should Be Executable
-------------------------
Fails if path is not an executable file for the current user.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

Get Cache Size
--------------
Get the cache size.

Get Inode
---------
Returns the inode number of a path.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

Get Version
-----------
Request the software version number.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - host
     - required
     - 
   * - port
     - required
     - 

Get Volume Id
-------------


.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name
     - required
     - 

Inode Should Be Equal
---------------------
Fails if path `a` is a different inode than `b`.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - a
     - required
     - 
   * - b
     - required
     - 

Link
----
Create a hard link.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - src
     - required
     - 
   * - dst
     - required
     - 
   * - code_should_be
     - 
     - 0

Link Count Should Be
--------------------
Fails if the inode link count is not `count`.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - count
     - required
     - 

Login
-----
Acquire an AFS token for authenticated access.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - user
     - required
     - 
   * - password
     - 
     - None
   * - keytab
     - 
     - None

Logout
------
Release the AFS token.

Mount Volume
------------
Mount an AFS volume.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - vol
     - required
     - 
   * - options
     - 
     - 

Pag From Groups
---------------
Return the PAG from the given group id list.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - gids
     - 
     - None

Pag Shell
---------
Run a command in the pagsh and returns the output.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - script
     - required
     - 

Pag Should Be Valid
-------------------
Fails if the given PAG number is out of range.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - pag
     - required
     - 

Pag Should Exist
----------------
Fails if a PAG is not set.

Pag Should Not Exist
--------------------
Fails if a PAG is set.

Release Volume
--------------


.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name
     - required
     - 

Remove Volume
-------------
Remove a volume.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name_or_id
     - required
     - 
   * - path
     - 
     - None
   * - flush
     - 
     - False
   * - server
     - 
     - None
   * - part
     - 
     - None
   * - zap
     - 
     - False

Should Be A Dump File
---------------------
Fails if filename is not an AFS dump file.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - filename
     - required
     - 

Should Be Dir
-------------
Fails if path is not a directory.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

Should Be File
--------------
Fails if path is not a file.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

Should Be Symlink
-----------------
Fails if path is not a symlink.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

Should Not Be Dir
-----------------
Fails if path is a directory.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

Should Not Be Symlink
---------------------
Fails if path is a symlink.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 

Symlink
-------
Create a symlink.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - src
     - required
     - 
   * - dst
     - required
     - 
   * - code_should_be
     - 
     - 0

Unlink
------
Unlink the directory entry.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - path
     - required
     - 
   * - code_should_be
     - 
     - 0

Volume Location Matches
-----------------------


.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name_or_id
     - required
     - 
   * - server
     - required
     - 
   * - part
     - required
     - 
   * - vtype
     - 
     - rw

Volume Should Be Locked
-----------------------
Verify the volume is locked.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name
     - required
     - 

Volume Should Be Unlocked
-------------------------
Verify the volume is unlocked.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name
     - required
     - 

Volume Should Exist
-------------------
Verify the existence of a read-write volume.

.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name_or_id
     - required
     - 

Volume Should Not Exist
-----------------------


.. list-table:: Arguments
   :header-rows: 1

   * - Name
     - 
     - Default value
   * - name_or_id
     - required
     - 

