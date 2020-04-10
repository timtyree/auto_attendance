### auto-attendence from Zoom meetings
Tim Tyree <br>
Dept. of Physics <br>
UCSD <br>
4.10.2020 <br>
Phys 2C Spring 2020

# Usage Guide
If you haven't yet checked out the 'Usage Guide.png' located in '/docs/', then do that now.  I made a lot of functionality that's hidden/minimally used, so I feel free to use it.  The primary functionality is performed using
$ ./setup.sh
$ ./take_attendance.sh

# Troubleshooting
* if the course roster has 'Sec ID' in a column other than A15, then you might need to change the default argument "skiprows = 14" to something else in get_my_students()
* if you don't have the command python3, try each of the following
$ brew install python
$ yum install python
$ apt-get install python
* if you get permission denied for executing the function <function.something>, then you can give that function permission to execute using
$ chmod +x <function.something>