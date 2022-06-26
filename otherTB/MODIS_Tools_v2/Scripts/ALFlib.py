
################################################################################
# ALFlib.py - Aggregated Live Feed library                                     #
#                                                                              #
# A collection of helper utility classes and functions designed to assist Live #
# Data Aggregation scripts.                                                    #
#                                                                              #
# Created by: Paul Dodd - esri, Software Product Release, Content Team         #
#    Contact: pdodd@esri.com                                                   #
#                                                                              #
#     Build: v2.4.0, June 2017, P.D.                                           #
#         - Patched 'getDownload' function to correct error during verbose use.#
#           Updated security to better handle authentication and cookie support#
#           internally. Repurposed 'authentication' property to provide an     #
#           alternate URI to authenticate user/password to.                    #
#         - Updated 'zipIt' function to support 7zip shared file compression.  #
#         - Added echo property to 'Logger' class in order to more easily      #
#           manage Console display activity setting. Added logging property to #
#           more easily manage logging of display content. Updated property    #
#           and method documentation details to match.                         #
#         - Added inclusions, exclusions, and recurse options to 'unzipIt'     #
#           function.                                                          #
#         - Added estimateCompletion method to Multi-processing worker pool,   #
#           accessible from 'Logger' Class. Updated 'faster/slower' stat to    #
#           include seconds for 'days' to support long running tasks.          #
#         - Patched getDownload function FTP restart logic, improving support. #
#         - Patched augmentEnvironment function to remove unicode value output.#
#     Build: v2.3.0, December 2016, P.D.                                       #
#         - Patched 'Logger' class to correct missing log file attachment when #
#           'Status' option is set and flag condition is raised. Added Caution #
#           Flag verbage to automated e-mail Subject details. Minor updates to #
#           internal StdOverride routine to update handler logic and write     #
#           timestamp details. Updated internal '_initOptions' function to     #
#           allow for application of non e-mail related environment variable   #
#           settings. Added 'timestamp' and 'showTimestamp' properties,        #
#           providing control of optional timestamp inclusion to activity log. #
#           Updated documentation. Updated 'waitForWorkers' function, adding   #
#           'elapsed time' reporting and ability to wait on Pools that are not #
#           closed (as long as <timeout> supplied) allowing for Auto-Closure   #
#           of open Pools if no additional work detected. Updated Worker Pool  #
#           statistics to include completion and wait time totals for Pool     #
#           that finishes last when waiting on multiple pools. Added display   #
#           of idle time for all Pools.                                        #
#         - Patched 'getDownload' function to correct cache control dictionary #
#           access issue. Updated to return I/O error '550 Permission Denied,  #
#           or No such file or folder' when file is not available. Updated to  #
#           enhance SSL support for Python v2.7.9+. Added <data> parameter.    #
#         - Updated 'check7zip' to return version details rather than True     #
#           when 7zip is found.                                                #
#         - Updated 'unzipIt' to leverage 7zip v15.05 or newer 'bb' logging    #
#           option to pickup name of files extracted. Also changed to return   #
#           an empty list on error, rather than False.                         #
#         - Added support for 'ALFlog_?' environment variables.                #
#         - Added verbose control to 'Progress' class.                         #
#         - Restuctured to remove Tab indentions in code. Better adhering to   #
#           Python standards.                                                  #
#     Build: v2.2.0, January 2016, P.D.                                        #
#         - Patched 'Logger' class to correct use/check of Alert Email limit,  #
#           consecutive tracking across periods, and single period day use.    #
#         - Updated 'Logger.setMailOption' method to support new 'verbose',    #
#           'tries', and 'delay' variables.                                    #
#         - Updated 'Logger.sendMail' method to support new mail options       #
#           internally and to return Boolean outcome on completion.            #
#         - Updated 'sendEmail' function to support multiple mail servers,     #
#           new 'tries' and 'delay' variables, and to support retry logic.     #
#           Also added 'details' option to enable return of outcome details    #
#           as a dictionary on successful send.                                #
#     Build: v2.1.0, December 2015, P.D.                                       #
#         - Updated 'Logger' class to support 'setFlag' caution condition and  #
#           method. Slight change to 'Status' reporting content for Flagged    #
#           runs. A flagged run is considered a success, but the prior state   #
#           will be kept until the next success or failure is encountered.     #
#           Allowing for persistent processing issues to be detected for       #
#           intermediate data updates regardless of run frequency. Added       #
#           environment augmentation to include optional '<nickname>_env.py'   #
#           file ingestion following default ingestion.                        #
#         - Updated 'augmentEnviron' function to support hierarchal environment#
#           file importation, applying last to first path order, when a non-   #
#           specific file and path is provided.                                #
#         - Patched 'copyFiles' function, correcting false source cannot equal #
#           destination message and exit.                                      #
#         - Added 'getEnviron' function to return Environment Variable values  #
#           as a desired object type.                                          #
#     Build: v2.0.2, November 2015, P.D.                                       #
#         - Patched 'Logger.setMailOption' function to honor Iterable values.  #
#           Better supporting address lists and tuples as it should.           #
#         - Softened messages from 'getNetworkDetails', as they exist merely   #
#           to provide insight and not to raise an alarm.                      #
#         - Patched 'sendEmail' function environ use to convert strings to     #
#           bool and int where appropriate.                                    #
#         - Updated 'augmentEnviron' function to allow date/time/datetime      #
#           variable types.                                                    #
#         - Updated 'getDownload' function to support cache control logic by   #
#           adding 'If-None-Match' request header for sites that supply 'Etag' #
#           response values and do not support the 'If-Modified-Since' request #
#           header. Reducing downloads of otherwise cacheable content.         #
#     Build: v2.0.1, October 2015, P.D.                                        #
#         - Patched 'Logger' internal mail initializer and 'getNetworkDetails' #
#           function to correct issue with missing or inaccessible content.    #
#         - Augmented 'sendEmail' function to allow sender address Alias.      #
#           Ex: 'ALF Process <pdodd@esri.com>', supported w/wo e-mail address. #
#           Also enabled recipient addresses and attachments to use Iterables. #
#         - Patched 'getDownload' function to set Binary mode for Size request.#
#     Build: v2.0.0, May 2015, P.D.                                            #
#         - Enhanced 'AppLock' class to allow multiple lock release attempts.  #
#           Unlock function now returns String containing release details.     #
#         - Patched 'getNetworkDetails' function to overcome Domain lookup     #
#           failure for non-existing Domains.                                  #
#         - Removed deprecated 'copyFileGDB' function.                         #
#         - Added 'iterPath' function. Revised 'getDownload', 'recursePath',   #
#           and 'zipIt' functions + 'Logger' class to use 'iterPath'.          #
#         - Enhanced internal '_formatTimeDelta' function by adding parameter  #
#           to allow verbose time text.                                        #
#         - Enhanced 'sendEmail' function to leverage 'ALFmail_' environment   #
#           variables for defaults when parameters not specified.              #
#         - Updated Logger class with 'exitReturnError' property. Invokes a    #
#           gracefully python exit when error conditions is detected at Log    #
#           closure, returning an error outcome value to initiating routine.   #
#           Added 'loadDetail' and 'saveDetail' functions, allowing long term  #
#           storage and retrieval of run specific objects to internal 'Detail' #
#           file.                                                              #
#     Build: v1.11.1, April 2015, P.D.                                         #
#         - Patched 'Logger' status logic to include status details if another #
#           e-mail type is being sent and to correct issue when changing hours #
#           in mail period setting.                                            #
#         - Patched 'unzipIt' function to fix issue with internal Zip library  #
#           when a file password is used.                                      #
#         - Altered 'Logger.waitForWorkers' timeout logic to improve accuracy. #
#         - Enhanced 'copyFiles' function by adding Elapsed Time reporting.    #
#         - Added internal '_formatTimeDelta' string format function.          #
#         - Altered all Time Delta displays to use new '_formatTimeDelta' func.#
#         - Altered 'AppLock' class, adding Try block to close in unlock func. #
#           To better harden logic, improving release/removal of lock file.    #
#         - Patched '_StdOverride' class, adding 'encoding' property for unix. #
#         - Patched Multiprocessing pool logic to better support Python 2.6.   #
#     Build: v1.11.0, March 2015, P.D.                                         #
#         - Patched 'sendEmail' func, correcting attachment encoding issue.    #
#         - Enhanced 'S3cmd.getInfo' method by adding variables to control the #
#           retry attempts and pause behavior.                                 #
#         - Added method documentation to 'S3cmd' class.                       #
#         - Corrected e-mail message spelling err in Logger 'atexitHook' func. #
#           Updated 'findMailServer' func, eliminating recursive Domain search #
#           behavior. Added 'status' to Logger e-mail send option.             #
#         - Enhanced 'getNetworkDetails' func, added 'findDomain' func to      #
#           obtain valid Domain. Added 'verbose' parameter and 'localDomain'   #
#           key to output Dictionary data.                                     #
#         - Added 'augmentEnviron' function to apply updates to local          #
#           Environment Variables while run is in progress. No need to alter   #
#           Global System environment variables and reboot!                    #
#     Build: v1.10.0, October 2014, P.D.                                       #
#         - Patched Multiprocessing '_Pool' class to correct stderr logging.   #
#         - Corrected 'getNetworkDetails' Doc spelling.                        #
#         - Added Keyword Argument support to 'retryIt' function.              #
#         - Added FTP and HTTP(S) restart capability to 'getDownload' func.    #
#           Increased default Buffer size to 8MB, improving transfer times.    #
#           Altered FTP logic to support Buffer usage. Altered 304 response    #
#           message 'Remote file has not changed...' to 'Remote file is older  #
#           than Local or has not change...'. Added 'headers' parameter to     #
#           allow user to set HTTP(S) request headers. Added request header    #
#           display when Verbose enabled.                                      #
#         - Added import of inspect library.                                   #
#         - Added return outcome detection and Exception passing to 'retryIt'  #
#           func. if retryHook supports arguments, the current Exception will  #
#           be passed in. If retryHook returns a non-empty result, retries are #
#           canceled.                                                          #
#         - Updated exception Hook in Logger class to report Exception details #
#           to Archive log.                                                    #
#         - Added import 'platform'                                            #
#         - Added 'retryIt' call to 'S3cmd.getInfo' method. Should allow S3    #
#           upload time to propagate file details before Info needs access.    #
#         - Added Elapsed Time outcome reporting to 'callCommandLine' func.    #
#     Build: v1.9.1, July 2014, P.D.                                           #
#         - Patched 'Logger' class _initMail method's processing of            #
#           'ALFmail_Limit' Environment Variable.                              #
#         - Added 'Recent Faults' to automated e-mail generation details,      #
#           reporting failure count for this period and for today.             #
#     Build: v1.9.0, May 2014, P.D.                                            #
#         - Added 'repr' method to OrderedDict class to support object content #
#           exploration.                                                       #
#         - Formally exposed the 'verbose' property.                           #
#         - Patched 'getDownload' function to bubble up error condition        #
#           triggered in certain cases.                                        #
#         - Enhanced 'getDownload' function to detect stale data sources when  #
#           timeStamping is set to a 'datetime.timedelta' object, throwing an  #
#           Exception to that effect. Also enhanced it to detect unknown remote#
#           file size, prompting a download / compare to local file when the   #
#           timeStamping option is enabled.                                    #
#         - Enhanced 'sendEmail' func to enable toAddr, ccAddr, and bccAddr    #
#           parameters to support a comma or semi-colon separated string       #
#           containing recipient addresses. Also expanded sensitivity parameter#
#           to include 'confidential'. Also added a subType param to allow     #
#           definition of text type, like plain; html; enriched; rtf; or other.#
#         - Added 'setMailOption' and 'sendMail' methods, environmental        #
#           variable detection, and E-mail support to 'Logger' class. Any      #
#           script using the Logger will now have E-mail notification          #
#           capability when ALFlib.py is upgraded.                             #
#         - Altered 'sendEmail' function to only report a file attachment's    #
#           name, not its Path.                                                #
#         - Added 'getNetworkDetails' function.                                #
#     Build: v1.8.0, April 2014, P.D.                                          #
#         - Patched 'heatIndex' function, fixing typo in one variable used by  #
#           calculation. Added more accurate alternate calculation when range  #
#           drops below 80 degrees. Added adjustment logic calculations to     #
#           primary algorithom.                                                #
#         - Added caseSensitive option to 'recursePath' function.              #
#         - Altered 'unzipIt' function to return list of extracted files on    #
#           success rather than True.                                          #
#         - Added property documentation and display logic when console help   #
#           option is used.                                                    #
#         - Updated 'getDownload' to allow timeStamping to force download and  #
#           file compare when set to None.                                     #
#         - Added 'sendEmail' SMTP mail function.                              #
#     Build: v1.7.0, January 2014, P.D.                                        #
#         - Patched 'getDownload' to remove residual text displayed.           #
#         - Refined 'getDownload' to report when access to remote file's       #
#           "last-modified" time is not available, relying on file size check  #
#           when timestamping is specified. For http-based requests, added     #
#          'If-Modified-Since' header allow server to issue 304-unchanged msg. #
#           Added '<', '~', and '>' to local/remote file size display details. #
#         - Altered 'unzipIt' and 'zipIt' functions to exclude 7zip '-p'       #
#           option when password is not specified.                             #
#         - Added newline to 'log' method of 'Logger' class, so it behaves     #
#           like the 'archive' method (and python print command).              #
#         - Added Multiprocessing support to 'Logger' class. Adding seperate   #
#           log file for each worker process. Added 'createWorkerPool'         #
#           function to support worker pool creation.                          #
#         - Added 'StopWatch' class.                                           #
#         - Added 'Spinner' class.                                             #
#         - Added 'progressBar' function.                                      #
#         - Updated 'CountryCodeLoader' class to use the UofVienna as a primary#
#           HTTP source and the data maintainer FTP.RIPE.NET as alternate.     #
#         - Added 'waitForWorkers' function to Logger.                         #
#         - Expanded 'OrderedDict' class, adding iteritem method.              #
#         - Added 'StateAbbreviations' lookup Dictionary to 'Constants' Class. #
#         - Added 'InitializationError' exception class.                       #
#         - Enhanced error logging to include Traceback Details!               #
#         - Patched 'zipIt' function, added recursive option to 7zip include   #
#           and exclude switches.                                              #
#         - Added 'retryIt' function.                                          #
#         - Added 'MultiprocessingError' class.                                #
#     Build: v1.6.1, April 2013, P.D.                                          #
#         - Patched 'Logger' to handler 'IOError: 32 - Broken Pipe' issue      #
#           experienced when running within a cron job. Traced to file 'flush' #
#           operations, probably caused by 'flushing' console write when there #
#           is nothing to flush!                                               #
#         - Updated 'copyFiles' function to report copy file issue, but not    #
#           throw an exception until completion of last file.                  #
#         - Updated 'callCommandLine' to allow masking of passwords when       #
#           command text is displayed.                                         #
#         - Updated 'zipIt' and 'unzipIt' functions to take advantage of       #
#           maskPassword option in 'callCommandLine' routine.                  #
#     Build: v1.6.0, April 2013, P.D.                                          #
#         - Added 'S3cmd' class.                                               #
#         - Added 'zipIt' function.                                            #
#         - Added 'getVerboseHandles' function.                                #
#         - Added 'recursePath' function.                                      #
#         - Added 'copyFiles' function.                                        #
#         - Added 'TimeoutError' exception class.                              #
#         - Added 'callCommandLine' function.                                  #
#         - Deprecated 'copyFileGDB' function in favor of 'copyFiles' function.#
#           Also added a deprecation message to function.                      #
#         - Updated 'unzipIt' function to leverage 'callCommandLine' function  #
#           and to unpack most any archive.                                    #
#         - Updated 'getDownload' function to support download of S3 content   #
#           using S3cmd class. Patched FTP logic to support an alternate query #
#           method for retrieving a file's size. Updated to leverage           #
#          'getVerboseHandles' and 'Progress'. Also added verbose option.      #
#         - Updated 'check7zip' func, adding handle for verbose message output.#
#         - Patched 'log' method in 'Logger' class to echo msg text to err log.#
#     Build: v1.5.1, November 2012, P.D.                                       #
#         - Patched getDownload 'basic' authentication.                        #
#         - Added 'unzipIt' function.                                          #
#         - Added 'setFileTime' function.                                      #
#     Build: v1.5.0, October 2012, P.D.                                        #
#         - Patched '_showInventory' routine to display more complex object    #
#           output, like 'version'.                                            #
#         - Added support for viewing library Property values.                 #
#           Ex: 'ALFlib.py desc', to return description of lib (see 'version').#
#         - Updated 'getDownload' function to handle secure FTP transfers and  #
#           to better detect source file details before transfer.              #
#     Build: v1.4.0, September 2012, P.D.                                      #
#         - Updated 'getDownload' function to handle URL responses that do not #
#           contain a last modified property. Also updated to support UNC and  #
#           Local file paths w/o needing to include 'FILE://' for source input.#
#         - For 'Logger' class: Added Flush statement to STD override outputs. #
#           Added 'close' method. Added 'log' method. Added 'setError' method. #
#         - Enhanced Inventory logic to be more dynamic and allow for calling  #
#           Functions from command line. Ex: 'ALFlib.py f2c 212' returns 100.0 #
#         - Added 'copyFileGDB' function.                                      #
#         - Added 'check7zip' function.                                        #
#     Build: v1.3.0, July 2012, P.D.                                           #
#         - Added 'Progress' class.                                            #
#         - Added ProjectionExtents to 'Constants' class.                      #
#         - Added 'DataError' Exception class.                                 #
#     Build: v1.2.0, June 2012, P.D.                                           #
#         - For 'Logger' class, added Flush statement to STD override handler. #
#         - Added 'getDownload' function.                                      #
#         - Added 'OrderedDict' class.                                         #
#         - Added 'xmlNormalizer' function.                                    #
#     Build: v1.1.0, May 2012, P.D.                                            #
#         - Added 'minVersion' function logic.                                 #
#         - Added 'AppLock' class logic.                                       #
#         - Update 'Logger' to Lock Premature exit file to overcome mutli-     #
#           instance execution. Supports graceful exit if more than one        #
#           instance attempts to run at the same time. Revised Premature exit  #
#           detection logic to deal with Lock file and parallel executions.    #
#           Added keepActivity logic to allow saving Log file when activity    #
#           logging is needed.                                                 #
#     Build: v1.0.3, April 2012, P.D.                                          #
#         - Restructured code to better adhere to Python standards and best    #
#           practices.                                                         #
#         - Version details available from namespace.                          #
#     Build: v1.0.2, April 2012, P.D.                                          #
#         - Patched: 'CountryCodeLoader' and 'WeatherStationLoader' to bubble  #
#                    up exceptions.                                            #
#         - Updated: Base class '_CacheLoader' to accept and test for an       #
#                    Alternate source URL.                                     #
#     Build: v1.0.1, April 2012, P.D.                                          #
#     Build: v1.0.0, March 2012, P.D.                                          #
#                                                                              #
# Depends on: Python v2.6+                                                     #
################################################################################

import atexit, collections, datetime, errno, filecmp, fnmatch, ftplib, inspect, json, locale, math, os, platform
import cookielib, shutil, socket, ssl, sys, subprocess, tempfile, time, traceback, urllib, urllib2, zipfile, zlib
import ALFlib as utils
import multiprocessing, multiprocessing.pool

# Version details directly available from namespace, as of v1.0.3
major = 2
minor = 4
bug = 0
desc = "v{0}.{1}.{2}, June 2017, Paul Dodd - esri".format( major, minor, bug)

# Add property specific documentation as '_<property>__doc__', for inventory display only!
_major__doc__ = """Property: major

    Gets the Major release number of this library as an integer.
"""

_minor__doc__ = """Property: minor

    Gets the Minor release number of this library as an integer.
"""

_bug__doc__ = """Property: bug

    Gets the Bug release number of this library as an integer.
"""

_desc__doc__ = """Property: desc

    Gets the release Description of this library as a string.
"""

verbose = None

_verbose__doc__ = """Property: verbose

    Gets or Sets the default Verbose display setting for objects in this library.

    Options include: True  - Display all detail (verbose at Maximum)
                     False - Never display anything (verbose is OFF)
                     None  - (default) Display minimal detail
"""

# Version function, for compatability
def version():
    """Function: version()

    Report version details for this library.

    Returns Dictionay that includes:
    {'Major': <num>, 'Minor': <num>, 'Bug': <num>, 'Desc': <description>}

    Properties also available from this library directly via <library>.<property>:
    Properties can be directly accessed by using <library>.<property>:
        '<library>.major' To get the Major release number.
        '<library>.minor' To get the Minor release number.
          '<library>.bug' To get the Bug fix level of release.
         '<library>.desc' To get the release description.
"""

    return { "Major": utils.major, "Minor": utils.minor, "Bug": utils.bug, "Desc": utils.desc}

# Report if ALFlib version is at least the requested minimum, new at v1.1.0
def minVersion( major=0, minor=0, bug=0):
    """Function: minVersion( [<major>[, <minor>[, <bug>]]])

    return True if this library version is at least the minimum
    specified by the input provided. False otherwise.

    Where:
        <major> = (optional) Major release number is at least this number.
                  Default is 0 (zero)

        <minor> = (optional) Minor release number is at least this number.
                  Default is 0 (zero)

          <bug> = (optional) Bug fix release number ia at least this number.
                  Default is 0 (zero)

    Example usage:

        import ALFlib

        # Verify ALFlib version, need at least v1.4.0
        if not (hasattr( ALFlib, "minVersion") and ALFlib.minVersion( 1, 4, 0)):
            del ALFlib
            raise Exception( "Found incompatible version of 'ALFlib.py' script, need at least v1.4.0 *")
"""

    if major and hasattr(major, 'isdigit') and major.isdigit():
        major = int(major)

    if minor and hasattr(minor, 'isdigit') and minor.isdigit():
        minor = int(minor)

    if bug and hasattr(bug, 'isdigit') and bug.isdigit():
        bug = int(bug)

    try:
        return ((major, minor, bug) <= (utils.major, utils.minor, utils.bug))
    except:
        return False

######################
# Assorted Constants #
######################

class Constants( object):
    """Class: Constants()

    Assorted Constants.

        'TrueNorth': Dictionary x-ref of Text Bearing ('N', 'S', 'SW',
                     'SSW', ...) to matching decimal degree.

        'ProjectionExtents': Dictionary of Point, Line, and Polygon Boundary
                             point lists used to construct Registration
                             Features by Projection ID.
                             Main Dictionary key is Projection number.
                             Dictionary value contains three Dictionaries:
                             'pointLayer', 'lineLayer', and 'polygonLayer'
                             each contains a list of X and Y points that make
                             up the Boundary Features.

        'StateAbbreviations': Dictionary of US State and Territory abbreviations
                              to Name lookup.
"""

    # True-North direction to degree x-ref. Paul Dodd, Mar 2012
    TrueNorth = {
        'N': 0,    # North
        'NbE': 11.25,	# North by East
        'NNE': 22.5,	# North, North-East
        'NEbN': 33.75,	# North-East by North
        'NE': 45,    # North-East
        'NEbE': 56.25,	# North-East by East
        'ENE': 67.5,	# East, North-East
        'EbN': 78.75,	# East by North
        'E': 90,    # East
        'EbS': 101.25,	# East by South
        'ESE': 112.5,	# East, South-East
        'SEbE': 123.75,	# South-East by East
        'SE': 135,    # South-East
        'SEbS': 146.25,	# South-East by South
        'SSE': 157.5,	# South, South-East
        'SbE': 168.75,	# South by East
        'S': 180,    # South
        'SbW': 191.25,	# South by West
        'SSW': 202.5,	# South, South-West
        'SWbS': 213.75,	# South-West by South
        'SW': 225,    # South-West
        'SWbW': 236.25,	# South-West by West
        'WSW': 247.5,	# West, South-West
        'WbS': 258.75,	# West by South
        'W': 270,    # West
        'WbN': 281.25,	# West by North
        'WNW': 292.5,	# West, North-West
        'NWbW': 303.75,	# North-West by West
        'NW': 315,    # North-West
        'NWbN': 326.25,	# North-West by North
        'NNW': 337.5,	# North, North-West
        'NbW': 348.75	# North by West
    }

    # Projection Boundary Features. Dictionary of Projections, containing a Dictionary of
    # Point, Line, and Polygon lists containing Features, each Feature contains a list of
    # Points, each Point contains an X and Y ordinate. Each Feature is a registration
    # Feature that marks the boundary (Min and Max data extent) of the Projection area.
    ProjectionExtents = {
        # Min and Max Latitudes for safe re-projection of WGS84 is -88.9999 and 88.9999
        4326: {
            'pointLayer': [
                [[-179.9999, -88.9999]],
                [[179.9999, 88.9999]]],
            'lineLayer': [
                [[-179.9999, -88.9949],	[-179.9999, -88.9999], [-179.9899, -88.9999]],
                [[179.9999, 88.9949], [179.9999, 88.9999], [179.9899, 88.9999]]],
            'polygonLayer': [
                [[-179.9999, -88.9999], [-179.9899, -88.9999], [-179.9899, -88.9949],
                 [-179.9949, -88.9949], [-179.9949, -88.9899], [-179.9999, -88.9899],
                 [-179.9999, -88.9999]],
                [[179.9999, 88.9999], [179.9899, 88.9999], [179.9899, 88.9949],
                 [179.9949, 88.9949], [179.9949, 88.9899], [179.9999, 88.9899],
                 [179.9999, 88.9999]]]
        }
    }

    # US state and territory abbreviations to name lookup. Paul Dodd, Dec 2013
    StateAbbreviations = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AS": "American Samoa",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "DC": "District of Columbia",
        "FM": "Federated States of Micronesia",
        "FL": "Florida",
        "GA": "Georgia",
        "GU": "Guam",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MH": "Marshall Islands",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "MP": "Northern Mariana Islands",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PW": "Palau",
        "PA": "Pennsylvania",
        "PR": "Puerto Rico",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VI": "Virgin Islands",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming"
    }

#####################
# Custom Exceptions #
#####################

class DataError( Exception):
    """Class: DataError( <exception text>)

    Custom Exception that can be Raised when a Data Exception has been
    encountered. Derived from the base Exception class.

    Where:
        <exception text> = (optional) text description of the Exception.
"""
    pass

class TimeoutError( Exception):
    """Class: TimeoutError( <exception text>)

    Custom Exception that is Raised when an expiration period has elapsed
    while waiting for an action, process, or call to return.
    Derived from the base Exception class.

    Where:
        <exception text> = (optional) text description of the Exception.
"""
    pass

class InitializationError( Exception):
    """Class: InitializationError( <exception text>)

    Custom Exception that is Raised when an Initialization process has failed.
    Derived from the base Exception class.

    Where:
        <exception text> = (optional) text description of the Exception.
"""
    pass

class MultiprocessingError( Exception):
    """Class: MultiprocessingError( <exception text>)

    Custom Exception that is Raised when a Multiprocessing error condition exists.
    Derived from the base Exception class.

    Where:
        <exception text> = (optional) text description of the Exception.
"""
    pass

######################################################
# Log File Manager                                   #
#                                                    #
# Overrides sys.stdout, sys.stderr, and sys.exit     #
# handlers. Echos content to Activity and Error logs.#
# Also traps and reports unhandled Exceptions,       #
# retaining error log if non-zero exit code or       #
# exception is detected.                             #
#                                                    #
# Output: Archive log as: <name>_YYYYMM.txt          #
#        Activity log as: <name>_LastRun.txt         #
#           Error log as: <errPath>\YYYYMMDD_HHMI.txt#
#                                                    #
# <name> = NickName used during class instantiation. #
# <errPath> = Folder called '<name>_Errors'          #
#                                                    #
# Build: v1.11.0, Feb 2015, Paul Dodd - esri         #
#     - Added incorporation of 'augmentEnviron'      #
#       function.                                    #
# Build: v1.7.0, May 2014, Paul Dodd - esri          #
#     - Added e-mail support.                        #
# Build: v1.6.0, Dec 2013, Paul Dodd - esri          #
#     - Added 'waitForWorkers' function.             #
# Build: v1.5.0, Aug 2013, Paul Dodd - esri          #
#     - Added Multiprocessing support, including the #
#       'createWorkerPool' function.                 #
#     - Added Unicode encoding support for Log Files.#
#     - Added 'loggerObject' property to StdOverride #
#       object. Allowing access to Logger object from#
#       sys.stdout/err handles.                      #
#     - Added 'getError' method.                     #
# Build: v1.4.0, May 2013, Paul Dodd - esri          #
#     - Added newline to 'log' method output, so it  #
#       behaves like the 'archive' method and python #
#       print command.                               #
# Build: v1.3.2, Apr 2013, Paul Dodd - esri          #
#     - Patched to handle IOERROR experienced during #
#       'flush' operations, when run within cron job.#
# Build: v1.3.1, Mar 2013, Paul Dodd - esri          #
#     - Patched 'log' method to echo message to      #
#       error log.                                   #
# Build: v1.3.0, Sep 2012, Paul Dodd - esri          #
#     - Added Flush statements to override outputs.  #
#     - Added 'close' method.                        #
#     - Added 'log' method.                          #
#     - Added 'setError' method.                     #
# Build: v1.2.0, May 2012, Paul Dodd - esri          #
#     - Added Flush statement to override handlers.  #
# Build: v1.1.0, May 2012, Paul Dodd - esri          #
#     - Added singleton logic to allow Premature     #
#       Exit file locking and graceful exit when     #
#       detected.                                    #
#     - Added 'keepActivity' property logic.         #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri          #
#     - Restructured code to better adhere to Python #
#       standards and best practices.                #
#     - Improved Exception handling and reporting.   #
# Build: v1.0.0, Mar 2012, Paul Dodd - esri          #
######################################################

class Logger( object):
    """Class: Logger( <nickName>, <homeFolder>[, <retention>[, <singleton>]])

    Initialize new <object> that will manage Log files for any script that
    instantiates this class. Activity Log will contain current run details.
    Archive Logs will contain summary of activity by month. Error Logs will
    contain copy of Activity Log for future review, and only retained if an
    Exception was found or Exit Code != 0. Expired Logs are removed as needed.

    Routine automatically traps Un-handled Exceptions and Script Exits with
    Exit Codes != 0 (logging them to the Archive and Error logs). Routine
    overrides Standard Out and Standard Error handlers, trapping any Printed
    message or reported error, logging all content.

    Also includes automatic E-mail capability to send notifications of process
    failures and updates. The e-mail log retains a history of mail activity.

    Where:
          <nickName> = (required) Name of routine that instantiates class.
                       Archive logs, Activity log, and ErrorLog folder will
                       be comprised of this name.

        <homeFolder> = (required) Home location where logs will be created.
                       Must have write access to this location.

         <retention> = (optional) Number of months to retain Log Files.
                       Default is 3, this month plus prior two.

         <singleton> = (optional) (True or False) Restrict run to a single
                       instance, gracefully terminating when Premature
                       exit Lock is detected. Exit will set status to -1
                       if Lock is detected.
                       Default is False.

    Methods:
        '<object>.archive( <str>, <boolean>)' Record <str> to Archive Log.

                           <str> = Text to be recorded.
                       <boolean> = True or False, echo <str> content to StdOut
                                   and Activity Log. (default) is False.

        '<object>.log( <str>)' Record <str> to Activity Log without echo to
                               StdOut.

                       <str> = Text to be recorded.

        '<object>.close()' Disconnect from Standard Out and Standard Error
                           handlers and close all Log files.

        '<object>.resetError()' Reset prior error condition, clearing error
                                detection and reporting at exit.

        '<object>.setError( <value>)' Set error condition, triggering error
                                      detection and reporting at exit.

        '<object>.getError()' Get current error condition if any.

        '<object>.setMailOption( <option>, <value>)' Set E-mail options used by
                                                     Logger object.

                                 <option> = String option (see setMailOption)
                                  <value> = Value for option (see setMailOption)

        '<object>.sendMail( <subject>, <body>, <attachments>, <importance>)'
                            Send E-mail using limited options here + stored
                            settings.

                                <subject> = String subject line of E-mail
                                   <body> = String content of E-mail body
                            <attachments> = String or List of String file paths
                                            of files to include as attachments.
                             <importance> = String 'Low', 'Normal', or 'High'

        '<object>.createWorkerPool( <initFunction>, <args>, <description>,
                                    <processCount>)' Create multiprocessing pool
                                                     of worker processes.

                                    <initFunction> = Optional initialization
                                                     function that will handle
                                                     initializing Processes.
                                            <args> = Optional arguments passed
                                                     to initializer fucntion.
                                     <description> = Optional description of
                                                     Worker Pool.
                                    <processCount> = Optional number of Worker
                                                     processes to create.

        '<object>.waitForWorkers( <workerPool>, <timeout>, <showProgress>,
                                  <detectExceptions>)' Wait for pool of workers
                                                       to complete their work.

                                        <workerPool> = createWorkerPool output
                                           <timeout> = Integer seconds or
                                                       timedelta to wait.
                                      <showProgress> = Display progress dialog?
                                  <detectExceptions> = Watch for any exceptions
                                                       generated by processes.

    Properties:
        From any routine using 'sys' module:
             'sys.stdout.log' True or False, to set default logging action.
                              Select whether or not to log messages by default.
            'sys.stdout.echo' True or False, to set default echo behavoir.
                              Select whether or not to echo messages to original
                              stream by default.
            'sys.stdout.write( <message>[, <logging>[, <echo>]])' Write message
                              directly to handle. Use optional parameters to
                              override current default settings for logging and
                              echo actions.
            'sys.stdout.writelines( <messages>[, <logging>[, <echo>]])' Same as
                              write method.
            (Same properties are available for 'sys.stderr'.)

        Other:
                    '<object>.echo' Same behavior as 'sys.stdout.echo', just a
                                    simpler way to set it. This will set the
                                    option on 'sys.stdout' and 'sys'stderr'

                 '<object>.logging' Same behavior as 'sys.stdout.log', just a
                                    simpler way to set it. This will set the
                                    option on 'sys.stdout' and 'sys'stderr'

            '<object>.keepActivity' True or False, instructs Logger to save and
                                    re-label the error log for posterity when a
                                    non-error exit is encountered. Appending
                                    '_activity' to the file name. Allowing the
                                    tracking of activity over time by using the
                                    existing log files.

               '<object>.timestamp' Get or Set the 'datetime.strftime' display
                                    mask used to format Date/Time timestamp
                                    added to front of all Activity Log entries.

             '<object>.exitMessage' Get or Set String text written to Activity
                                    Log during exit. As a final message or note.

         '<object>.exitReturnError' Get or Set Python exit behavior when error
                                    condition is detected at Log closure. If set
                                    to True, Logger will initiate a graceful
                                    exit of Python, returning error to calling
                                    routine, providing an exit outcome value.
                                    Default is False
"""
    def __init__( self, nickName, homeFolder, retention=3, singleton=False):
        home = os.path.realpath( homeFolder)

        self._logFolder = home
        self._keepActivity = False
        self._closing = False
        self._exitReturnError = False
        self._timestamp = ""
        self._showTimestamp = True
        # Standard Override properties
        self._startTime = datetime.datetime.now()
        self._lastTime = self._startTime
        self._hadNewline= True

        # Does home exist?
        if not os.access( home, os.F_OK):
            try:
                # Try to create home folder
                os.makedirs( home)

            except Exception as e:
                raise IOError( "* Unable to create Log path: '{0}', {1}".format( home, e))
        else:
            # Do we have Write permission?
            if not os.access( home, os.W_OK):
                raise IOError( "* Unable to write to Log path: '{0}'".format( home))

        errorFolder = os.path.join( home, nickName + '_Errors')

        # Does error log folder exist?
        if not os.access( errorFolder, os.F_OK):
            os.mkdir( errorFolder)

        # Check for Premature Exit Detection file
        self._earlyExit = os.path.join( errorFolder, 'PreMatureExitDetection.tmp')
        if os.access( self._earlyExit, os.F_OK):
            earlyExit = datetime.datetime.fromtimestamp( os.stat( self._earlyExit).st_mtime)
            earlyExit = os.path.join( errorFolder, earlyExit.strftime( '%Y%m%d_%H%M%S.txt'))
        else:
            earlyExit = False

        self.StopWatch = utils.StopWatch()
        #self.StopWatch.start()

        now = self.StopWatch.start()
        # Create Premature Exit file immediately after taking note of date/time
        try:
            self._singleton = utils.AppLock( lockfile=self._earlyExit)
            if not self._singleton.lock():
                # Not an early exit, prior process still running!
                if singleton:
                    # Requested single process execution!
                    print( " * Unable to Lock Premature exit file, single instance of app requested, exiting!")
                    sys.exit(-1)
                else:
                    # Turn off singleton, do NOT disturb existing early exit file!
                    self._singleton = False
                    earlyExit = "Process still running"
        except Exception as e:
            self._singleton = False
            raise Exception( " * Error: Unable to create Application Lock on Premature Exit file: {0}".format( e))

        # Setup log names
        self._activityLog = os.path.join( home, nickName + '_LastRun.txt')

        archiveFmt = nickName + '_%Y%m.txt'	# Filename Format mask used by DateTime format and Cleanup
        archiveMask = nickName + '_2*.txt'	# Search Mask for Log Cleanup
        self._archiveLog = os.path.join( home, now.strftime( archiveFmt))

        # v1.7.0
        mailFmt = nickName + '_EmailLog_%Y%m.txt'	# Filename Format mask used by DateTime format and Cleanup
        mailMask = nickName + '_EmailLog_2*.txt'	# Search Mask for Log Cleanup
        self._mailLog = os.path.join( home, now.strftime( mailFmt))
        self._detailFile = os.path.join( home, nickName + "_Details.json")
        self._tmpDetailFile = os.path.join( home, "~" + nickName + "_Details.tmp")
        self._nickName = nickName
        #

        errorFmt = '%Y%m%d_%H%M%S.txt'	# Filename Format mask used by DateTime format and Cleanup
        errorMask = '2*.txt'    # Search Mask for Log Cleanup
        self._errorLog = os.path.join( errorFolder, now.strftime( errorFmt))

        # Open Log files
        self._archiveFP = open( self._archiveLog, 'a')
        self._errorFP = open( self._errorLog, 'w')
        self._activityFP = open( self._activityLog, 'w')

        # Save and Override StdOut and StdErr
        sys.stdout = self._StdOverride( self._activityFP, sys.stdout, self._errorFP, self)
        utils.stdout = sys.stdout
        sys.stderr = self._StdOverride( self._activityFP, sys.stderr, self._errorFP, self)
        utils.stderr = sys.stderr

        # Do not echo errors to screen
        sys.stderr.echo = False

        # Setup Hooks for Exceptions and Exit
        self._applyHooks()

        # Act on Prior Run Premature exit state
        if earlyExit:
            if earlyExit == "Process still running":
                # Note additional process detected
                self.archive( "\n* Note * Detected parallel process running *", True)
                earlyExit = False
            else:
                # Merge any left over Multiprocess Log files that may exist
                with open( earlyExit, "a") as oFP:
                    logfile = os.path.splitext( earlyExit)
                    self._mergeWorkerLogs( logfile[0] + "_*" + logfile[1], oFP)

                # Alert to Premature exit
                self.archive( "\n* Detected Premature exit by prior run *", True)
                self.archive( "  For details see: '{0}'".format( earlyExit), False)

        # Display startup details
        title = "\n{0} Routine Started: {1}".format( nickName, now.strftime( '%H:%M:%S %a %m/%d/%Y'))
        self.archive( title, True)
        self.archive( '-' * (len(title) - 1), True)

        # v1.11.0, Apply Augmented Environment Variable changes
        utils.augmentEnviron()
        # v2.1.0, Apply Augmented Environment Variables for 'nickname' environment file
        utils.augmentEnviron( "{0}_env.py".format( nickName))

        # v1.7.0, setup initial Logger options from environment
        self._initOptions()
        if earlyExit:
            # Save early exit log path for end of process e-mail checks
            self._mailOptions[ "earlyExit"] = earlyExit

        # Cleanup Log Files
        month = now.year * 12 + now.month - retention
        year = month / 12
        month = month - (year * 12) + 1
        ageOut = datetime.datetime( year, month, 1)	# Remove anything older than this
        self._trimLogs( ageOut, home, archiveMask, archiveFmt)
        self._trimLogs( ageOut, home, mailMask, mailFmt)
        self._trimLogs( ageOut, errorFolder, errorMask, errorFmt)

        # Final __init__ logic, apply timestamp property
        if hasattr( self, "_timestampDelay"):
            self.timestamp = self._timestampDelay
            del self._timestampDelay

    # Handle final reporting and close out Worker Pool objects and resources!
    def _closeWorkers( self):
        """Internal method, not intended for general consumption!"""

        if hasattr( self, '_workerPoolRegistry'):
            for workerPool in self._workerPoolRegistry.itervalues():
                try:
                    workerPool.terminate()
                except:
                    pass

                # Patched for Python 2.6 compatibility
                workerPool._processes = len( workerPool._pool)

                # Compute percentages
                total = (workerPool.sumTime.days + workerPool.idleTime.days) * 86400 + (workerPool.sumTime.seconds + workerPool.idleTime.seconds)   # Includes seconds per day
                elapsed = 0.0 if not total else 1.0 - (float(workerPool.elapsedTime.days * 86400 + workerPool.elapsedTime.seconds) / total)   # Compute % difference
                idle = 0.0 if not total else float(workerPool.idleTime.seconds) / total                 # Compute percentage

                # Display stats
                self.archive( "Pool: '{0}', workers: {1}, tasks: {2}/{3}, time: {4}(min) {5}(max) {6}(avg) {7}(idle) {8}(sum) {9}(tot) {10:1.0%}(diff)".format(
                    workerPool.description,
                    workerPool._processes,
                    workerPool.workSucceeded,
                    workerPool.workSubmitted,
                    utils._formatTimeDelta( workerPool.minTime),
                    utils._formatTimeDelta( workerPool.maxTime),
                    utils._formatTimeDelta( workerPool.avgTime),
                    utils._formatTimeDelta( workerPool.idleTime),
                    utils._formatTimeDelta( workerPool.sumTime),
                    utils._formatTimeDelta( workerPool.elapsedTime),
                    abs( elapsed)))

                if self.exitMessage:
                    self.exitMessage += "\n"
                self.exitMessage += "The '{0}' pool of {1} worker{2} successfully completed {3} out of {4} task{5}:\n      Work Completed at: {6}{7}\n     Shortest task time: {8}\n  Average time per task: {9}\n      Longest task time: {10}\n        Total idle time: {11} ({12:1.0%})\n  Total processing time: {13}\n      Pool elapsed time: {14} ({15:1.0%}{16})\n".format(
                    workerPool.description,
                    workerPool._processes,
                    "s" if not workerPool._processes == 1 else "",
                    workerPool.workSucceeded,
                    workerPool.workSubmitted,
                    "s" if not workerPool.workCompleted == 1 else "",
                    "N/A" if workerPool.workEnded == workerPool.poolCreated else workerPool.workEnded,
                    "" if not hasattr( workerPool, "waitTime") else " * Waited {0} for completion *".format( utils._formatTimeDelta( workerPool.waitTime, stripStr="")),
                    utils._formatTimeDelta( workerPool.minTime, stripStr=""),
                    utils._formatTimeDelta( workerPool.avgTime, stripStr=""),
                    utils._formatTimeDelta( workerPool.maxTime, stripStr=""),
                    utils._formatTimeDelta( workerPool.idleTime, stripStr=""),
                    abs( idle),
                    utils._formatTimeDelta( workerPool.sumTime, stripStr=""),
                    utils._formatTimeDelta( workerPool.elapsedTime, stripStr=""),
                    abs( elapsed),
                    " little change" if abs(elapsed) <= 0.005 else " faster" if elapsed > 0.0 else " slower")
            del self._workerPoolRegistry

    def close( self):
        """Method: Close out logging actvity and file storage.

    Terminate any active worker processes, consolidate log files,
    and restore Standard output handlers prior to instantiation.
 """
        if not self._closing:
            if self.timestamp:
                # Turn off logging timestamp
                self.timestamp = ""

            self._closing = True
            self._closeWorkers()

            sys.exitfunc()	# invoke ALFlog exit function
            if hasattr( self, '_origExit'):
                sys.exit = self._origExit
                del self._origExit
            if hasattr( self, '_origExcepthook'):
                sys.excepthook = self._origExcepthook
                del self._origExcepthook
            if hasattr( utils.stderr, '_origFp'):
                sys.stderr = utils.stderr._origFp
                del utils.stderr
            if hasattr( utils.stdout, '_origFp'):
                sys.stdout = utils.stdout._origFp
                del utils.stdout

    @property
    def keepActivity( self):
        """Property: Get or Set activity log retension indicator.

    True or False, whether or not to keep activity logs for successful processes.
"""
        return self._keepActivity

    @keepActivity.setter
    def keepActivity( self, value):
        if type( value) == type( True):
            self._keepActivity = value

    @property
    def exitMessage( self):
        """Property: Get or Set text 'Exit Message' string added to e-mail outcome notifications."""
        return getattr( self, "_exitMSG", "")

    @exitMessage.setter
    def exitMessage( self, value):
        if isinstance( value, basestring):
            self._exitMSG = value

    @property
    def exitReturnError( self):
        """Property: Get or Set error exit outcome.

    True or False, whether or not to return an error exit value when available.
"""
        return self._exitReturnError

    @exitReturnError.setter
    def exitReturnError( self, value):
        if type( value) == type( True):
            self._exitReturnError = value

    def archive(self, message, echo=False):
        """Method: Record <message> text to Archive Log, controlling whether to
    echo text to Console or not.
"""
        if isinstance( message, unicode):
            message = u"{0}\n".format( message)
        else:
            message = "{0}\n".format( message)

        if self._archiveFP:
            if hasattr( self, "lockObject"):
                self.lockObject.acquire()

            try:
                if isinstance( message, unicode) and getattr( sys.stdout, "_encoding", None):
                    # Encode using same encoing as stdout
                    self._archiveFP.write( message.encode( sys.stdout._encoding))
                else:
                    self._archiveFP.write( message)

                self._archiveFP.flush()
            except:
                if hasattr( self, "lockObject"):
                    self.lockObject.release()
                raise

            if hasattr( self, "lockObject"):
                self.lockObject.release()

        if echo:
            utils.stdout.write( message, echo=True)

    def log(self, message):
        """Method: Record <message> text to Activity Log without echoing to Console.
"""
        if isinstance( message, unicode):
            message = u"{0}\n".format( message)
        else:
            message = "{0}\n".format( message)

        utils.stderr.write( message, logging=True)

    @property
    def echo( self):
        """Property: Get or Set the 'echo' state of the Console display.

    True or False, whether to enable or disable Console display, logging
    will still be enabled without Console output.

    Warning, setting is applied to both 'sys.stdout' and 'sys.stderr' handlers!
"""
        return utils.stdout.echo

    @echo.setter
    def echo( self, enable):
        utils.stdout.echo = enable
        utils.stderr.echo = enable

    @property
    def logging( self):
        """Property: Get or Set the 'logging' state of display actions.

    True or False, whether to enable or disable logging action, selecting
    whether or not to log displayed messages.

    Warning, setting is applied to both 'sys.stdout' and 'sys.stderr' handlers!
"""
        return utils.stdout.log

    @logging.setter
    def logging( self, enable):
        utils.stdout.log = enable
        utils.stderr.log = enable

    @property
    def timestamp( self):
        """Property: Get or Set the 'datetime.strftime' string mask used to
    format Date/Time timestamp added to front of all Activity Log entries.

    Also supports '{e}' and '{l}' mask substitution for reporting ELAPSED
    time and time since LAST message in floating point seconds, great for
    process or function timing without altering your existing logic.

    Example masks and results prepended to log entries:
        '[%Y/%m/%d %H:%M:%S.%f] - ' prepends '[2016/09/11 09:22:10.501000] - '
                 '[%H:%M:%S.%f] - ' prepends '[09:22:10.501000] - '
                    '[%M:%S.%f] - ' prepends '[22:10.501000] - '
                    '[{e}][{l}] - ' prepends '[4.291][0.230] - '
                  '[%M:%S][{l}] - ' prepends '[22:10][0.230] - '

    For complete options See:
        docs.python.org/2.7/library/datetime.html#strftime-strptime-behavior
"""
        return self._timestamp

    @timestamp.setter
    def timestamp( self, mask):
        if mask and isinstance( mask, basestring):
            try:
                if datetime.datetime.now().strftime( mask):
                    self._timestamp = mask
            except Exception as e:
                sys.stderr.write( " * Failed to set ALFlog timestamp to '{0}': {1}\n".format( mask, e))
        else:
            self._timestamp = ""

    @property
    def showTimestamp( self):
        """Property: Enable or Disable display of Timestamp in Activity Log."""
        return self._showTimestamp

    @showTimestamp.setter
    def showTimestamp( self, enable):
        self._showTimestamp = True if enable else False

    # Remove Log files older than 'expireDate' and report deletion to Archive Log
    def _trimLogs( self, expireDate, logPath, logMask, logFormat):
        """Internal method, not intended for general consumption!"""

        expireFormat = expireDate.strftime( logFormat)

        for file in os.listdir( logPath):
            if fnmatch.fnmatch( file, logMask):
                if file < expireFormat:
                    fileName = os.path.join( logPath, file)
                    self.archive( "* Deleting Log: '{0}'".format( fileName))
                    os.remove( fileName)

    # Apply Hooks to Exception and Exit handlers
    def _applyHooks(self):
        """Internal method, not intended for general consumption!"""

        def exceptionHook( type, value, tb):
            print( "\n* Un-handled Exception Detected *")

            if self.timestamp:
                # Turn off logging timestamp
                self.timestamp = ""

            if hasattr( sys.stderr, "echo"):
                echoWas = sys.stderr.echo
                sys.stderr.echo = True

            sys.stderr.write( '\n')
            traceback.print_exception( type, value, tb)
            sys.stderr.write( '\n')

            if not self._exitValue:	# Report error in Archive on first encounter
                self.archive( "* Un-handled Exception Detected, details: '{0}', error: '{1}' *".format( self._errorLog, self._exitValue))

            if hasattr( sys.stderr, "echo"):
                sys.stderr.echo = echoWas

            self._exitValue = Exception( value)

        def exitHook( value=0):
            # Fired before 'atexit' Hook when 'sys.exit' invoked, save Exit value
            self._exitValue = value
            self._forcedExit = True
            self.close()

        def atexitHook():
            # Setup Exit message to append to e-mail body
            exitMsg = ""
            if self.exitMessage:
                exitMsg = "\n\nExit Message: " + self.exitMessage

            # Load Exit value, 'exitHook' not fired if clean exit and 'sys.exit' not invoked
            value = self._exitValue
            self._closeWorkers()

            if self._singleton:
                # Release Application Lock on early exit file
                outcome = self._singleton.unlock()
                if outcome:
                    self.archive( "* 'AppLock.unlock' Outcome: {0}".format( outcome))

            startDatetime = self.StopWatch.startTime    # Get Date/Time of begining
            td = startDatetime - datetime.datetime( 1970, 1, 1)
            startTimestamp = float(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

            # Load mail period Details and initialize values
            periodSize = self._mailOptions.get( "period", 4)
            periods = int(23 / periodSize) + 1
            mailDate = startDatetime.strftime( "%Y/%m/%d")
            mailPeriod = startDatetime.hour / periodSize
            mailSubject = ""
            mailBody = ""
            mailAttachments = self._activityLog if self._mailOptions.get( "status", (0, False))[1] else ""   # Attach activity log if required
            mailImportance = "Normal"
            mailState = 0  # 0 = Success, 1 = Failure, 2 = Prior run premature exit failure
            mailStatus = True   # Status Outcome: True is Good, False is Bad
            mailCounter = {}    # Period counter details, will be last or current period

            mailDetails = {} # Current Mail Details
            fileDetails = {} # Mail Details loaded from File

            # Load current Mail Period details
            try:
                fileDetails = self.loadDetail( "email")

            except Exception as e:
                sys.stderr.write( "\n * {0} *\n".format( e))

            # Set Details/Defaults from File Copy
            mailDetails[ "LastDate"] = fileDetails.get( "LastDate", mailDate)
            mailDetails[ "LastPeriod"] = fileDetails.get( "LastPeriod", mailPeriod)
            mailDetails[ "LastState"] = fileDetails.get( "LastState", 0)
            mailDetails[ "LastStart"] = fileDetails.get( "LastStart", startTimestamp)
            mailDetails[ "Consecutive"] = fileDetails.get( "Consecutive", 0)
            mailDetails[ "FailureEmails"] = fileDetails.get( "FailureEmails", 0)
            mailDetails[ "FailureSent"] = fileDetails.get( "FailureSent", False)
            mailDetails[ "DayCounters"] = fileDetails.get( "DayCounters", {})
            mailDetails[ "PeriodCounters"] = fileDetails.get( "PeriodCounters", [])

            del fileDetails # Remove Loaded file details, no longer needed

            # Setup Period Counter details if missing or incorrect, a rolling window of counters by period
            if not isinstance( mailDetails[ "PeriodCounters"], list) or len( mailDetails[ "PeriodCounters"]) != periods or mailDetails[ "LastPeriod"] >= periods:
                mailDetails[ "PeriodCounters"] = []
                mailDetails[ "LastPeriod"] = mailPeriod
                for item in range( periods):
                    mailDetails[ "PeriodCounters"].append( {"Failures": 0, "Successes": 0, "Flags": 0, "IntervalSeconds": 0, "TotalSeconds": 0, "MinSeconds": 0, "MaxSeconds": 0})

            # Setup Day Counter details if missing
            if not isinstance( mailDetails[ "DayCounters"], dict) or not mailDetails[ "DayCounters"]:
                mailDetails[ "DayCounters"] = {"Failures": 0, "Successes": 0, "Flags": 0, "IntervalSeconds": 0, "TotalSeconds": 0, "MinSeconds": 0, "MaxSeconds": 0}

            # Setup Flags and Pointers
            lastPeriod = mailDetails[ "LastPeriod"]
            lastCounter = mailDetails[ "PeriodCounters"][ lastPeriod]   # Get Last Period Counters
            periodCounter = mailDetails[ "PeriodCounters"][ mailPeriod] # Get This Period Counters
            dayCounter = mailDetails[ "DayCounters"]                    # Get Daily Counters
            dayReset = (mailDetails[ "LastDate"] != mailDate)
            periodReset = (lastPeriod != mailPeriod) or dayReset # include dayReset to handle one period a day!
            mailCounter = periodCounter     # Default mailCounter is current period counter
            initPeriod = mailPeriod         # Default initMailBody period

            # Flag status action overrides
            dayStatus = (dayReset and self._mailOptions.get( "status", (0, False))[0]) # and not mailPeriod)
            periodStatus = (periodReset and self._mailOptions.get( "status", (0, False))[0] > 1)
            allStatus = (self._mailOptions.get( "status", (0, False))[0] == 3)
            #includeLog = self._mailOptions.get( "status", (0, False))[1]   # Removed v2.2.1

            # Check state of run and report exceptions if needed
            if value:
                msg = ""
                detected = ""
                if not isinstance( value, BaseException):
                    detected = "Error Exit"
                    if isinstance( value, basestring):
                        msg = "* {0} detected: {1} *".format( detected, value)
                    else:
                        msg = "* {0} '{1}' detected *".format( detected, value)
                else:
                    value = str( value)
                    detected = "Un-handled Exception"
                    msg = "* {0} detected: '{1}' *".format( detected, value)

                print( "\n{0}".format( msg))
                self.archive( "* {0} detected, for details see: '{1}' *".format( detected, self._errorLog))

                # Setup failure e-mail
                mailSubject = "Alert: Routine '{0}' encountered a problem".format( self._nickName)
                mailAttachments = self._errorLog
                mailBody = msg + exitMsg
                mailImportance = "High"
                mailState = 1  # Failure
                mailStatus = False  # Bad
                # Check for and add consecutive failure message to body of e-mail
                if not periodReset and mailDetails[ "Consecutive"]:
                    mailBody += "\n\n* Routine has failed {0} times in a row! *".format( mailDetails[ "Consecutive"] + 1)

            elif self._mailOptions.get( "earlyExit", False):
                # No errors, but setup prior run premature exit e-mail
                mailSubject = "Alert: Routine '{0}' discovered a Premature Exit".format( self._nickName)
                mailAttachments = self._mailOptions[ "earlyExit"]
                mailBody = "* Latest run was successful, but detected a Premature exit by Prior run *"
                mailImportance = "High"
                mailState = 2  # Premature exit failure
                mailStatus = False  # Bad

            elif not self._flagValue:
                # No errors or Flags raised
                #mailAttachments = self._activityLog if includeLog else ""   # Attach activity log if required # Removed v2.2.1
                mailImportance = "Low"

                # Check if prior run failed, then setup Success e-mail
                if self._mailOptions.get( "success", True) and mailDetails[ "FailureSent"]:
                    mailSubject = "Update: Routine '{0}' returned to a successful state".format( self._nickName)
                    mailBody = "Routine executed successfully following a previous failure."

            # Check if we need to add status details!
            if dayStatus or periodStatus or allStatus:
                if not mailSubject:
                    # Set Status Summary subject if not already set to something
                    mailSubject = "Status: Routine '{0}' completed successfully".format( self._nickName)

                if mailBody:
                    # Add line spacing to body
                    mailBody += "\n\n"

                if dayStatus or periodStatus:
                    # Place Counter Headers here
                    msg = "\n\nPeriod:Hrs  Successes  Failures  Flags  Avg Interval    Min Time     Max Time     Avg Time\n"
                    msg +=    "----------  ---------  --------  -----  ------------  -----------  -----------  -----------\n"

                    if not mailBody:
                        # Override current period to last period
                        mailCounter = lastCounter
                        initPeriod = lastPeriod

                    if dayStatus:
                        # Loop thru all Counters
                        for index, item in enumerate( mailDetails[ "PeriodCounters"]):
                            fromHr = periodSize * index
                            toHr = (fromHr + periodSize) if fromHr + periodSize < 24 else 24
                            msg += reportStat( "{0}: {1:02}-{2:02}".format( index, fromHr, 24 if toHr > 24 else toHr), item) + "\n"
                        msg += reportStat( "Day: 00-24", dayCounter) + "\n"

                        mailBody += "Status Summary for last Day - " + mailDetails[ "LastDate"] + msg
                    else:
                        # Report last Period Counter
                        fromHr = periodSize * lastPeriod
                        toHr = (fromHr + periodSize) if fromHr + periodSize < 24 else 24
                        msg += reportStat( "{0}: {1:02}-{2:02}".format( lastPeriod, fromHr, toHr), lastCounter) + "\n"
                        msg += reportStat( "Day: 00-24", dayCounter) + "\n"

                        mailBody += "Status Summary for last Period" + msg
                else:
                    # Must be allStatus
                    mailBody += "Status for last Run"

            mailBody = self._initMailBody( mailBody, mailAttachments, mailStatus, mailCounter, dayCounter, initPeriod, periodSize)

            elapsedTime = self.StopWatch.stop()
            elapsedSeconds = (elapsedTime.days * 86400) + elapsedTime.seconds + ( float( elapsedTime.microseconds) / 1000000)

            if self._flagValue:
                # Report caution flag
                self.archive( "* Caution Flag: {0} *".format( self._flagValue))
                if mailSubject:
                    mailSubject += " w/'{0}' Caution".format( self._flagValue)

            if self.timestamp:
                # Turn off logging timestamp
                self.timestamp = ""

            msg = "Finished: {0} (Elapsed Time: {1})".format( datetime.datetime.now().strftime( '%H:%M:%S %a %m/%d/%Y'), utils._formatTimeDelta( elapsedTime, stripStr=""))
            sys.stderr.write( "\n{0}\nRoutine {1}\n".format( "-" * (len( msg) + 8), msg))
            self.archive( msg)

            if hasattr( self, "_errorLogMask"):
                msg = " Multiprocessing Statistics "
                sys.stderr.write( "\n#{0}#\n".format( "#" * len( msg)))
                sys.stderr.write( "#{0}#\n".format( msg))
                sys.stderr.write( "#{0}#\n".format( "#" * len( msg)))

            if self.exitMessage:
                sys.stderr.write( "\n{0}".format( self.exitMessage))

            if hasattr( self, "_errorLogMask"):
                # Merge Multiprocessing log content into main Log files
                self._mergeWorkerLogs( self._errorLogMask, sys.stderr)

            # Reset counters if Date or Period has changed!
            resetCounters = []
            if dayReset:
                mailDetails[ "LastDate"] = mailDate
                resetCounters = mailDetails[ "PeriodCounters"][0:]  # Copy pointer to Period Counters
                resetCounters.append( mailDetails[ "DayCounters"])  # Add pointer to Day Counters

            if periodReset:
                mailDetails[ "LastPeriod"] = mailPeriod
                if mailDetails[ "Consecutive"] >= self._mailOptions.get( "consecutive", 1):
                    # Reset consecutive count if greater than or equal to limit
                    mailDetails[ "Consecutive"] = 0
                # Reset Email count
                mailDetails[ "FailureEmails"] = 0
                resetCounters.append( periodCounter)

            # Reset counters identified!
            for counter in resetCounters:
                counter[ "Flags"] = 0
                counter[ "Failures"] = 0
                counter[ "Successes"] = 0
                counter[ "IntervalSeconds"] = 0
                counter[ "TotalSeconds"] = 0
                counter[ "MinSeconds"] = 0
                counter[ "MaxSeconds"] = 0

            # Increment mail counters and verify we can still send e-mail
            if mailState:   # Only valid for Failure or Premature exit
                dayCounter[ "Failures"] += 1
                periodCounter[ "Failures"] += 1
                mailDetails[ "Consecutive"] += 1

                ignorable = not (dayStatus or periodStatus or allStatus)

                # Check for limits and conditions that would block sending an e-mail
                if ignorable and mailDetails[ "FailureEmails"] >= self._mailOptions.get( "limit", 3):
                    self._mailOptions[ "Ignored"] = "Failure eMail limit exceeded"
                elif ignorable and mailDetails[ "Consecutive"] < self._mailOptions.get( "consecutive", 1):
                    self._mailOptions[ "Ignored"] = "Consecutive Failures below threashold"
                elif ignorable and mailDetails[ "Consecutive"] > self._mailOptions.get( "consecutive", 1):
                    self._mailOptions[ "Ignored"] = "Consecutive Failures above threashold"
                else:
                    # A Failure or Premature Exit E-mail WILL be sent!
                    # Set sent status based on state of e-mail being sent, True for Failure and False for Premature
                    mailDetails[ "FailureSent"] = (mailState == 1)
                    mailDetails[ "FailureEmails"] += 1
            elif self._flagValue:
                # Flag raised, skip normal success logic
                #dayCounter[ "Flags"] += 1
                dayCounter[ "Flags"] = dayCounter.get( "Flags", 0) + 1
                #periodCounter[ "Flags"] += 1
                periodCounter[ "Flags"] = periodCounter.get( "Flags", 0) + 1
            else:
                # A Success E-mail could be sent
                # Reset Consecutive error count and Failure Sent status
                mailDetails[ "Consecutive"] = 0
                mailDetails[ "FailureSent"] = False
                dayCounter[ "Successes"] += 1
                periodCounter[ "Successes"] += 1

            # Set Day and Period Second Counters
            for counter in [ dayCounter, periodCounter]:
                counter[ "IntervalSeconds"] = counter.get( "IntervalSeconds", 0) + (startTimestamp - mailDetails[ "LastStart"])
                counter[ "TotalSeconds"] += elapsedSeconds
                if not counter.get( "MinSeconds", 0) or elapsedSeconds < counter[ "MinSeconds"]:
                    counter[ "MinSeconds"] = elapsedSeconds
                if not counter.get( "MaxSeconds", 0) or elapsedSeconds > counter[ "MaxSeconds"]:
                    counter[ "MaxSeconds"] = elapsedSeconds

            # Send the e-mail and save Period Details
            if mailSubject:
                if not (self.sendMail( mailSubject, mailBody, mailAttachments, mailImportance, "enriched") or value):
                    # Save log on e-mail failures!
                    value = "sendMail Failure"

            try:
                # Save current values not already saved
                mailDetails[ "LastState"] = mailState
                mailDetails[ "LastStart"] = startTimestamp

                # Save Mail Period details to file
                self.saveDetail( mailDetails, "email")

            except Exception as e:
                sys.stderr.write( "\n * {0} * \n".format( e))
            #

            if not value:
                # Clean exit, no need to keep Error Log so remove it,
                # unless keep activity has been set to True!
                if self._errorFP:
                    self._errorFP.close()
                    self._errorFP = False

                try:
                    if not self._keepActivity:
                        # Remove it!
                        os.remove( self._errorLog)
                    else:
                        # Rename it!
                        path, filename = os.path.split( self._errorLog)
                        name, ext = filename.split('.')
                        activityFile = os.path.join( path, name + '_activity.' + ext)
                        os.rename( self._errorLog, activityFile)
                except:
                    if hasattr( self, "_errorLogMask"):
                        print( "* Multiprocessing enabled - were all Worker pools closed and joined before exit?")
                    raise

            if self._archiveFP:
                self._archiveFP.close()
                self._archiveFP = False

            if self._errorFP:
                self._errorFP.close()
                self._errorFP = False

            if self._activityFP:
                self._activityFP.close()
                self._activityFP = False

            sys.exit = self._origExit
            if value and (self._forcedExit or self._exitReturnError):
                # if sys.exit is called or 'exitReturnError' flag is set, exit Python gracefully returning error value
                sys.exit( value)

        def reportStat( stat, detail):
            # Report Statistical data from period or day stat, return single line of text to include in e-mail
            totRuns = detail.get( "Successes", 0) + detail.get( "Failures", 0) + detail.get( "Flags", 0)
            times = {
                "Interval": 0.0 if not totRuns else float( detail.get( "IntervalSeconds", 0)) / totRuns,
                "Average": 0.0 if not totRuns else float( detail.get( "TotalSeconds", 0)) / totRuns,
                "Minimum": float( detail.get( "MinSeconds", 0)),
                "Maximum": float( detail.get( "MaxSeconds", 0))
            }

            # Period Successes Failures AvgInterval MinTime MaxTime AvgTime
            return "{0: >10}  {1: 9}  {2: 8}  {3: 5}  {4: >12}  {5: >11}  {6: >11}  {7: >11}".format(
                stat,
                detail.get( "Successes", 0),
                detail.get( "Failures", 0),
                detail.get( "Flags", 0),
                utils._formatTimeDelta( datetime.timedelta( seconds=times[ "Interval"]), decPlaces=2, stripStr=""),
                utils._formatTimeDelta( datetime.timedelta( seconds=times[ "Minimum"]), decPlaces=2, stripStr=""),
                utils._formatTimeDelta( datetime.timedelta( seconds=times[ "Maximum"]), decPlaces=2, stripStr=""),
                utils._formatTimeDelta( datetime.timedelta( seconds=times[ "Average"]), decPlaces=2, stripStr=""))

        self._flagValue = False         # Set initial Flag value
        self._exitValue = False    	# Set initial Exit value
        self._forcedExit = False        # Set initial 'forced' exit flag, set when 'sys.exit' used
        self._origExit = sys.exit    # Save current Exit handle
        sys.exit = exitHook    	# Override Exit handle
        atexit.register( atexitHook)    # Register Exit Hook
        self._origExcepthook = sys.excepthook	# Save current Excepthook
        sys.excepthook = exceptionHook	# Override Exception handle

    # v1.7.0, Initialize Logger options and validation logic
    def _initOptions( self):
        """Internal method, not intended for general consumption!"""

        def toPort( value):
            value = int( value)
            if value < 0 or value > 65535:
                raise Exception( "value out of range: 0-65535")
            return value

        def toPeriod( value):
            value = int( value)
            if value < 1 or value > 24:
                raise Exception( "value out of range: 1-24")
            return value

        def toFile( value):
            if not (os.path.exists( value) and os.path.isfile( value)):
                raise Exception( "file not found")
            return value

        def toBool( value):
            if value:
                if isinstance( value, basestring) and (value.lower() == "false" or value == "0"):
                    return False
                return True
            return False
            #return not (not value or value.lower() == "false" or value == "0")

        def toInt( value):
            value = int( value)
            if value < 1:
                raise Exception( "value out of range: > 0")
            return value

        def toStatus( value):
            includeLog = ("-" not in value)
            value = value.lower().strip( " +-")
            status = { "": 0, "day": 1, "period": 2, "run": 3}
            if not value in status:
                raise Exception( "value out of range: Not 'Day', 'Period', or 'Run'")
            return (status[ value], includeLog) # Return Tuple (<status level>, <log inclusion flag>)

        def toActivity( value):
            self.keepActivity = toBool( value)
            return True

        def toTimestamp( value):
            self._timestampDelay = value
            return True

        if not hasattr( self, "_mailOptions"):
            self._mailOptions = {}

            # Setup allowed e-mail options and their handler or type, used by setMailOption function
            self._validMailOptions = { # All lower case keys!
                "server": unicode, "port": toPort, "timeout": toInt, "ssl": toBool, "key": toFile, "certificate": toFile, "username": unicode, "password": unicode, "from": unicode,
                "to": unicode, "cc": unicode, "bcc": unicode, "sensitivity": unicode, "enabled": toBool, "period": toPeriod, "limit": toInt, "consecutive": toInt, "success": toBool,
                "status": toStatus, "verbose": toBool, "tries": toInt, "delay": toInt
            }

            # Local option Lookup dictionary
            options = {
                "alflog": {
                    "timestamp": toTimestamp,
                    "keepactivity": toActivity
                },
                "alfmail": self.setMailOption
            }

            # Check Environment Varibles for initial defaults or overrides
            optionsFound = False
            sys.stderr.write( "\nChecking Environment for applicable variables:\n")
            for key, value in os.environ.iteritems():
                group, option = (key.lower().split( "_", 1) + [''])[:2]
                if group in options:
                    if callable( options[ group]):
                        if options[ group]( option, value):
                            optionsFound = True
                    elif option in options[ group]:
                        if callable(options[ group][ option]):
                            if options[ group][ option]( value):
                                optionsFound = True
                                sys.stderr.write( " - Setting {0} option: '{1}' as '{2}'...\n".format( group, option, "********" if option == "password" else value))

            if not optionsFound:
                sys.stderr.write( " * No valid entries found...\n")
            sys.stderr.write( "\n")

    # v1.7.0, Initialize Mail message Body content
    def _initMailBody( self, message=None, attachments=None, goodStatus=None, recentDict={}, dailyDict={}, period=0, periodSize=4):
        """Internal method, not intended for general consumption!"""

        net = utils.getNetworkDetails( verbose=False)
        now = datetime.datetime.utcnow().strftime( "%a %b %d, %H:%M:%S %Y")
        periods = 23 / periodSize   # 0 to 23 hours

        color = ("green" if goodStatus else "black" if goodStatus is None else "red")

        mailBody = u"""<NoFill><Fixed><Smaller>
       Timestamp: <Bold>[{0} UTC]</Bold>
        Log Path: <Bold>'{1}'</Bold>
        Nickname: <Bold>'{2}'</Bold>
        Hostname: <Bold>'{3}'</Bold>, IP: <Bold>{4}</Bold>
    Ext DNS Name: <Bold>'{5}'</Bold>, IP: <Bold>{6}</Bold>
    Recent Flags: <Bold>{7}</Bold> for period {13}(0~{14}@{15}hr/ea), <Bold>{8}</Bold> today
   Recent Faults: <Bold>{9}</Bold> for period {13}(0~{14}@{15}hr/ea), <Bold>{10}</Bold> today
Recent Successes: <Bold>{11}</Bold> for period {13}(0~{14}@{15}hr/ea), <Bold>{12}</Bold> today""".format(
            now,
            self._logFolder,
            self._nickName,
            net.get( "localName", " * Unknown * "),
            net.get( "localAddr", " * Unknown * "),
            net.get( "externalName", " * Unknown * "),
            net.get( "externalAddr", " * Unknown * "),
            recentDict.get( "Flags", 0),
            dailyDict.get( "Flags", 0),
            recentDict.get( "Failures", 0),
            dailyDict.get( "Failures", 0),
            recentDict.get( "Successes", 0),
            dailyDict.get( "Successes", 0),
            period,
            periods,
            periodSize
        )

        if attachments:
            if not isinstance( attachments, list):
                attachments = [attachments]
            files = ""
            spacer = ""
            for item in attachments:
                files += "{0}'{1}'".format( spacer, unicode( item).split( self._logFolder)[-1])   # Strip leaves off right most character, use split!
                spacer = ", "

            mailBody += u"""
     Attachments: <Bold>{0}</Bold>""".format( files)

        if message:
            mailBody += u"""

Message detail:
---------------

<Color><Param>{0}</Param>{1}</Color>""".format( color, unicode( message).replace( "<", "&LT;").replace( ">", "&GT;"))

        if attachments:
            mailBody += u"""

---------------
<Bold>Please review attachments!</Bold>"""

        return mailBody + u"</Smaller></Fixed></NoFill>"

    # v1.7.0, Set allowed E-Mail options
    def setMailOption( self, option, value):
        """Method: setMailOption( <option>, <value>)

    Set allowed E-Mail option.

    Returns True if option was set successfully or False if an issue was logged.

    Where <option> and <value> can be any of the following:

             'server' = Name or IP of SMTP mail server
                        Environment Variable: 'ALFmail_Server'
               'port' = TCP port number used by connection. 0-65535
                        Environment Variable: 'ALFmail_Port'
            'timeout' = Number of seconds to wait for connection to complete
                        Environment Variable: 'ALFmail_Timeout'
                'ssl' = True or False to enable or disable secure connection usage
                        Environment Variable: 'ALFmail_SSL'
                'key' = Filename to private key file used by SSL
                        Environment Variable: 'ALFmail_Key'
        'certificate' = Filename to certificate chain file used by SSL
                        Environment Variable: 'ALFmail_Certificate'
           'username' = SMTP user account name
                        Environment Variable: 'ALFmail_Username'
           'password' = SMTP user account password
                        Environment Variable: 'ALFmail_Password'
               'from' = Sender's e-mail address
                        Environment Variable: 'ALFmail_From'
                 'to' = E-mail recipients
                        Environment Variable: 'ALFmail_To'
                 'cc' = Carbon Copy e-mail recipients
                        Environment Variable: 'ALFmail_CC'
                'bcc' = Bind Carbon Copy e-mail recipients
                        Environment Variable: 'ALFmail_BCC'
        'sensitivity' = Sensitivity level - 'normal', 'private', 'personal', or
                        'company-confidential' (or simply 'confidential').
                        Environment Variable: 'ALFmail_Sensitivity'
            'enabled' = True or False to enable or disable E-mail option
                        Environment Variable: 'ALFmail_Enabled'
             'period' = Number of hours in an e-mail period. Limited to 24 hours
                        Environment Variable: 'ALFmail_Period'
              'limit' = Number of Failure e-mails that can be sent in one period
                        Environment Variable: 'ALFmail_Limit'
        'consecutive' = Number of consecutive failures that must exist before an
                        e-mail can be sent.
                        Environment Variable: 'ALFmail_Consecutive'
            'success' = True or False to enable or disable e-mail reply on first
                        successful run following a failure e-mail.
                        Environment Variable: 'ALFmail_Success'
             'status' = 'Day', 'Period', or 'Run' to enable e-mail summary status
                        triggered when run starts a new day, a new period, or
                        when run is completed regardless of outcome. Add a '-'
                        to instruct status e-mail process NOT to include a copy
                        of the current activity log as an attachment.
                        Environment Variable: 'ALFmail_Status'
            'verbose' = True or False to enable or disable recording of SMTP
                        conversation with 'server'.
                        Environment Variable: 'ALFmail_Verbose'
              'tries' = Number of connection attempts that should be allowed
                        before giving up.
                        Environment Variable: 'ALFmail_Tries'
              'delay' = Number of seconds to wait between connection attempts.
                        Environment Variable: 'ALFmail_Delay'

    * Note * a <value> of None will remove setting, allowing the default. Please
             see 'sendEmail' function for more specific details.

    * Tip * To control multiple processes, set the system wide Environment
            Variables. All scripts that use the Logger will immediately leverage
            the e-mail option should a failure be encountered.

            When first instantiated, the Logger will look for and apply any e-mail
            specific Environment Variable it finds. Any changes made there after
            will override the values initially set.
"""
        if option:
            option = str( option).lower()
            if option in self._validMailOptions:
                try:
                    if value is None:
                        if option in self._mailOptions:
                            del self._mailOptions[ option]
                        sys.stderr.write( " - Defaulting E-mail option: '{0}'...\n".format( option))
                    else:
                        if isinstance( value, list) or isinstance( value, tuple): # v2.0.2
                            value = ", ".join( value)                             # v2.0.2
                        self._mailOptions[ option] = self._validMailOptions[ option]( unicode( value))
                        sys.stderr.write( " - Setting E-mail option: '{0}' as '{1}'...\n".format( option, "********" if option == "password" else self._mailOptions[ option]))

                    return True

                except Exception as e:
                    sys.stderr.write( " * Invalid E-mail value for option: '{0}', error: '{1}' - ignored!\n".format( option, e))
            else:
                sys.stderr.write( " * Invalid E-mail option: '{0}' - ignored!\n".format( option))

        return False

    # v1.7.0, Send E-mail using stored mail options
    def sendMail( self, subject, body="", attachments=(), importance="normal" or "low" or "high", subType="plain"):
        """Method: sendMail( <subject>[, <body>[, <attachments>[, <importance>[, <subType>]]]])

    Send E-mail using stored settings and options included here.

    Activity will be recorded to the e-mail log.

    Where:

            <subject> = String containing text Subject line of the e-mail.
               <body> = (optional) String containing text Body of e-mail.
        <attachments> = (optional) String or list of Strings containing paths to
                        files that will be included as attachments to e-mail.
         <importance> = (optional) String that specifies importance of e-mail.
            <subType> = (optional) String that specifies the subtype of the <body>
                        text. Like 'plain', 'html', 'enriched', 'rtf', or other.

    Returns:
                True  = When successful or when eMail is ignored
                False = When there is a failure
"""

        msg = ""
        outcome = None

        try:
            sys.stderr.write( "\n * Starting E-mail process *\n   Subject: {0}\n\n".format( subject))

            # Handle mail delivery
            with open( self._mailLog, "a") as oFP:
                oFP.write( "\n[{0}]\n".format( datetime.datetime.now().strftime( "%Y/%m/%d %H:%M:%S")))

                toAddr = self._mailOptions.get( "to", ())
                ccAddr = self._mailOptions.get( "cc", ())
                bccAddr = self._mailOptions.get( "bcc", ())

                if self._mailOptions.get( "enabled", True) and (toAddr or ccAddr or bccAddr):
                    if self._mailOptions.get( "Ignored", False):
                        msg = ' - E-mail IGNORED - {0}, Subject: "{1}"'.format( self._mailOptions[ "Ignored"], subject)
                        oFP.write( msg + "\n")
                        outcome = True
                    else:
                        server = self._mailOptions.get( "server", "")
                        port = self._mailOptions.get( "port", ())
                        timeout = self._mailOptions.get( "timeout", 30)
                        ssl = self._mailOptions.get( "ssl", False)
                        key = self._mailOptions.get( "key", None)
                        certificate = self._mailOptions.get( "certificate", None)
                        username = self._mailOptions.get( "username", "")
                        password = self._mailOptions.get( "password", "")
                        fromAddr = self._mailOptions.get( "from", "")
                        sensitivity = self._mailOptions.get( "sensitivity", "normal")
                        verbose = self._mailOptions.get( "verbose", None)
                        tries = self._mailOptions.get( "tries", 3)
                        delay = self._mailOptions.get( "delay", 5)

                        try:
                            outcome = sendEmail(	fromAddr, toAddr, subject, body, ccAddr, bccAddr, attachments, importance, sensitivity, server, port, username, password, ssl, key, certificate, timeout, verbose, subType, tries, delay, True)
                            msg = ' - E-mail SENT, Server: "{1}", Try: {2}, Subject: "{0}"'.format( subject, outcome[ "Server"], outcome[ "Attempt"])
                            oFP.write( msg + "\n")
                            if toAddr:
                                oFP.write( "         To: '{0}'\n".format( toAddr))
                            if ccAddr:
                                oFP.write( "         CC: '{0}'\n".format( ccAddr))
                            if bccAddr:
                                oFP.write( "        BCC: '{0}'\n".format( bccAddr))
                            if attachments:
                                if not isinstance( attachments, list):
                                    attachments = [attachments]
                                files = ""
                                spacer = " "
                                for item in attachments:
                                    files += "{0}'{1}'".format( spacer, unicode( item).split( self._logFolder)[-1])   # Strip leaves off right most character, use split!
                                    spacer = ", "
                                oFP.write( "Attachments: [{0}]\n".format( files))

                            outcome = True

                        except Exception as e:
                            msg = ' * E-mail FAILED * Subject: "{0}"'.format( subject)
                            oFP.write( "{0}\n   Error: '{1}'\n".format( msg, e))
                            sys.stderr.write( "{0}\n   Error: '{1}'\n\n".format( msg, e))
                            outcome = False
                else:
                    msg = ' - E-mail Option DISABLED - Ignoring message w/Subject: "{0}"'.format( subject)
                    oFP.write( msg + "\n")
                    outcome = True

        except Exception as e:
            msg = " * Failed to send E-mail: '{0}' *".format( e)
            sys.stderr.write( "\n" + msg + "\n")
            outcome = False

        finally:
            if msg:
                self.archive( msg)

            return outcome

    # Handle Logger Detail file load/save action
    def loadDetail( self, key="user"):
        """Method: loadDetail( [<key>])

    Loads Logger Detail file, returning specified <key> content. Can be used to
    store and retrieve run specific details that require long term retention.

    Returns:
        Data object identified by <key>. Can return Dictionary, List, or any
        other object supported by Json library load function. If <key> is not
        found, an empty Dictionary will be returned.

    Exceptions:
        A general exception will be thrown if there is an issue reading details
        from Detail file. The file path and exception details will be included.

    Where:
        <key> = (optional) User defined storage name. A Dictionary key used to
                store object details in Json format.
                Default key name is 'user'
"""
        if not (key and isinstance( key, basestring)):
            # key must be a string!
            key = "user"
        else:
            key = key.lower()

        details = {}

        try:
            if hasattr( self, "_detailFile") and os.access( self._detailFile, os.R_OK):
                with open( self._detailFile, "r") as iFP:
                    details = json.load( iFP)

        except Exception as e:
            raise Exception( "FAILED to load Details from file: '{0}', error: '{1}'".format( self._detailFile, e))

        if "version" not in details:
            # Assume initial release of Detail file, simply used to store Email Details!
            details = {"version": 2.0, "email": details}

        if key == "\\":
            # Return entire content, root level detail!
            return details

        return details.get( key, {})

    def saveDetail( self, obj, key="user"):
        """Method: saveDetail( <obj>[, <key>])

    Saves <obj> to Logger Detail file keyed by specified <key> name. Can be
    used to store and retrieve run specific details that require long term
   	retention. Can store any object support by Json library dump fucntion.

    Exceptions:
        A general exception will be thrown if there is an issue saving details
        to Detail file. The file path and exception details will be included.

    Where:
        <key> = (optional) User defined storage name. A Dictionary key used to
                store object details in Json format.
                Default key name is 'user'
"""
        if not (key and isinstance( key, basestring)):
            # key must be a string!
            key = "user"
        else:
            key = key.lower()

        details = {"version": 2.0}

        try:
            details = self.loadDetail( "\\")

        except Exception as e:
            sys.stderr.write( "\n * IGNORING * {0} *\n".format( e))

        details[ key] = obj

        try:
            with open( self._tmpDetailFile, "w") as oFP:
                json.dump( details, oFP, indent=3, separators=(",", ": "))

            try:
                if os.access( self._detailFile, os.F_OK):
                    os.remove( self._detailFile)

                os.rename( self._tmpDetailFile, self._detailFile)

            except Exception as e:
                raise Exception( "Unable to rename temporary Detail file, {0}".format( e))

        except Exception as e:
            raise Exception( "FAILED to save Details: '{0}'".format( e))

    def setFlag( self, value):
        """Method: Set Caution Flag condition (non-error)"""
        self._flagValue = value
        self.log( "\n * Caution Flag set to: '{0}' at {1}".format( value, datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S")))

    def resetError( self):
        """Method: Clear or Reset current error condition"""
        self._exitValue = False

    def setError( self, value):
        """Method: Set an error condition"""
        self._exitValue = value

    def getError( self):
        """Method: Get current error condition"""
        return self._exitValue

    # Setup a Multiprocess Worker Pool, supporting a seperate Log file for each process
    def createWorkerPool( self, initFunction="", args=(), description="", processCount=0):
        """Method: createWorkerPool( [<initFunction>[, <args>[, <description>[, <processCount>]]]])

    Create an enhanced Multiprocessing Pool that is supported by the Logger class.
    Which can be used to assign Asynchronous work items to a queue that is then
    processed by the worker processes created by the Pool.

    Returns:
        ALFlib._Pool object, an enhanced 'multiprocessing.pool.Pool' object.

    Where:
        <initFunction> = (optional) User defined Initialization Function to transfer
                         control to, one that will 'initialize' the new process(es).
                         Default is None, no initialization function will be invoked.
                <args> = (optional) Tuple or List of arguments to pass to <initFunction>.
                         Default is None, no arguments will be passed.
         <description> = (optional) User supplied Name or Description to add to Pool details.
                         Default will initially be the name 'Asynchronous'.
        <processCount> = (optional) Number of process workers to create.
                         If Negative, uses total CPUs - <processCount>.
                         If Less than 1, a fraction, uses <processCount> as Percentage of
                         available CPUs.
                         Default is the number of reported CPUs. Minimum used is 1
"""
        if not processCount:
            # Default, set to total CPUs
            processCount = multiprocessing.cpu_count()
        elif processCount < 0:
            # Negative, set to total CPUs - value
            processCount = int( multiprocessing.cpu_count() + processCount)
        elif processCount < 1:
            # Percentage, set to percentage of total CPUs
            processCount = int( multiprocessing.cpu_count() * processCount)

        if processCount < 1:
            # Do not allow value less than 1
            processCount = 1

        if not hasattr( sys.stdout, "lockObject"):
            sys.stdout.lockObject = multiprocessing.Lock()
            sys.stderr.lockObject = multiprocessing.Lock()
            self.lockObject = multiprocessing.Lock()

        logfile = os.path.splitext( self._errorLog)
        self._errorLogMask = logfile[0] + "_*" + logfile[1]

        if not hasattr( self, '_workerPoolRegistry'):
            self._workerPoolRegistry = {}

        # Setup Description
        if not description:
            description = "Asynchronous"

        tmpDescription = description
        tmpCnt = 1
        while tmpDescription in self._workerPoolRegistry:
            tmpCnt += 1
            tmpDescription = "{0}-{1}".format( description, tmpCnt)
        description = tmpDescription

        sys.stderr.write( "\nInitializing Pool of {0} '{1}' worker process(s)...\n".format( processCount, description))

        pool = _Pool( processCount, _initWorkerPool, [ self._errorLog, description, self.timestamp, initFunction, args])

        pool.description = description

        self._workerPoolRegistry[ description] = pool

        return pool

    # Merge Multiprocess Worker Log files with existing log files
    def _mergeWorkerLogs( self, logfileMask, fileHandle):
        """Internal method, not intended for general consumption!"""

        filePath, fileMask = os.path.split( logfileMask)

        msg = ""

        for workerLog in iterPath( filePath, fileMask):
            msg = "# Worker Process Log: '{0}' #".format( os.path.basename( workerLog))
            fileHandle.write( "\n" + "#" * len( msg) + "\n")
            fileHandle.write( msg + "\n")
            fileHandle.write( "#" * len( msg) + "\n")

            try:
                with open( workerLog, "r") as iFP:
                    for line in iFP.readlines():
                        fileHandle.write( line)

                try:
                    # Remove worker log after recording content
                    os.remove( workerLog)

                except Exception as e:
                    fileHandle.write( "\n * Note * Unable to remove Worker logfile, Error: '{0}'\n".format( e))

            except Exception as e:
                fileHandle.write( "\n * Failed to read Worker logfile, Error: '{0}'\n".format( e))

        if msg:
            fileHandle.write( "\n" + "#" * len( msg) + "\n")

    ##############################################
    # Wait for Worker Pool Processes to finish   #
    #                                            #
    # Build: v1.1.0, Sep 2016, Paul Dodd - esri  #
    #      - Added override to allow open worker #
    #        Pool when <timeout> supplied.       #
    # Build: v1.0.0, Nov 2013, Paul Dodd - esri  #
    ##############################################

    def waitForWorkers( self, workerPool=None, timeout=None, showProgress=True, detectExceptions=True):
        """Method: waitForWorkers( [<workerPool>[, <timeout>[, <showProgress>[, <detectExceptions>]]]])

        Waits for Worker Pool Processes to complete tasks assigned while reporting progress of
        work remaining. Also checks and reports any exit failures.

        Requires that monitored Pools are closed, unless <timeout> supplied!

        Returns:
            True on successful completion of all work.
            False if no pools exist or if workers terminate before all work has been completed.

        Exceptions:
            'TimeoutError' is raised if <timeout> enabled.
            'MultiprocessingError' is raised when a worker process exits with
            a state other than 0 (when 'detectExceptions' is True).
            Other general Exceptions can also be raised.

        Where:
                  <workerPool> = (optional) Multiprocessing worker Pool or list of
                                 worker Pools.
                                 Default is None, no specific Pool, so wait for all
                                 existing Pools
                     <timeout> = (optional) Integer seconds or datetime.timedelta to
                                 wait. If there is a lack of work progress in this
                                 time frame, a TimeoutError exception is thrown.
                                 Default is None, No Timeout
                <showProgress> = (optional) True or False. Specify whether or not to
                                 display progress to console.
                                 Default is True
            <detectExceptions> = (optional) True or False. If True, function will
                                 look for Exceptions logged by Worker processes and
                                 throw an Exception to the calling process.
                                 Default is True
	"""
        spin = utils.Spinner()

        start = datetime.datetime.now()
        last = start

        if timeout:
            if isinstance( timeout, int) or isinstance( timeout, long):
                timeout = datetime.timedelta( seconds=timeout)
            elif not isinstance( timeout, datetime.timedelta):
                raise Exception( "Input type missmatch for 'waitForWorkers' on field 'timeout', expected number or timedelta, received '{0}'".format( type( timeout)))

        if workerPool is None:
            if not (hasattr( self, '_workerPoolRegistry') and self._workerPoolRegistry):
                sys.stdout.write( u"\n * No worker pools available to wait for!\n")
                return False
            else:
                workerPool = self._workerPoolRegistry.values()

        if not isinstance( workerPool, list):
            workerPool = [ workerPool]

        for pool in workerPool:
            if not isinstance( pool, utils._Pool):
                raise Exception( "'workerPool' contains incompatible Pool objects, please correct!")
            if pool._state not in ( multiprocessing.pool.CLOSE, multiprocessing.pool.TERMINATE) and not timeout:
                raise Exception( "Cannot wait on Worker Pool '{0}', please close it first or supply a <timeout>".format( pool.description))

        workSubmitted = len( workerPool)
        workCompleted = 0
        processCount = True
        lastCount = -1
        lastPercent = -1.0
        lastMsgLen = 0
        workRemainingText = ""

        while processCount:
            workSubmitted = 0
            workCompleted = 0
            processCount = 0
            remainingWork = []
            openPools = []
            ectLast = False
            for Pool in workerPool:
                workSubmitted += Pool.workSubmitted
                workCompleted += Pool.workCompleted
                remainingWork.append( Pool.workRemaining)
                ect = Pool.estimateCompletion( True)
                if (not ectLast) or ect > ectLast:
                    ectLast = ect
                for process in Pool._pool:
                    if process.is_alive():
                        processCount += 1
                        openPools.append( Pool)
                    elif process.exitcode:
                        if detectExceptions:
                            try:
                                Pool.terminate()
                            except:
                                pass
                            sys.stdout.write( "\n")
                            raise utils.MultiprocessingError( "Worker pid-{0} failed with exit code '{1}'".format( process.pid, process.exitcode))
                        else:
                            # Just make note of failure
                            if not getattr( process, "reported", False):
                                sys.stderr.write( "\n * Worker pid-{0} failed with exit code '{1}'\n".format( process.pid, process.exitcode))
                                setattr( process, "reported", True)

            if openPools and (workSubmitted - workCompleted) < 1:
                # No work left to do, close open Pools!
                processCount = 0    # Clear Process counter, allowing wait to terminate
                for Pool in openPools:
                    loop = 3
                    while loop and Pool._state == multiprocessing.pool.RUN:
                        try:
                            self.log( "\n * Closing open Pool '{0}', no additional work available!".format( Pool.description))
                            Pool.close()
                            break
                        except Exception as e:
                            loop -= 1
                            if loop:
                                self.log( " * Failed to close Pool, retrying: {0}".format( e))
                                time.sleep( 5)
                    else:
                        if not loop:
                            self.log( " * Unable to close Pool, initiating termination...")
                            try:
                                Pool.terminate()
                            except:
                                pass

            if detectExceptions and self.getError():
                sys.stdout.write( "\n")
                raise utils.MultiprocessingError( self.getError())

            percent = 0.0
            if workSubmitted:
                percent = float( workCompleted) / workSubmitted

            if (workSubmitted + workCompleted + processCount) != lastCount or percent != lastPercent:
                lastCount = workSubmitted + workCompleted + processCount
                lastPercent = percent
                last = datetime.datetime.now() # Reset last time when there is activity!
                workRemainingText = u"Work remaining by Pool: {0} - {1}".format( remainingWork, utils.progressBar( percent))
            else:
                if timeout:
                    if (last + timeout) < datetime.datetime.now():
                        sys.stdout.write( "\n")
                        raise utils.TimeoutError( "Inactivity Timeout reached while waiting for Worker Processes")

            if showProgress:
                msg = "{} {} ECT [{}]".format( spin.next, workRemainingText, datetime.timedelta( ectLast.days, ectLast.seconds))
                sys.stdout.write( "\r{}{}\r".format( msg, "" if len(msg) >= lastMsgLen else " " * (lastMsgLen - len(msg))), logging=False)
                lastMsgLen = len(msg)

            time.sleep( 0.25)

        # v2.3.0
        waitMsg = ""
        if len( workerPool) > 1:
            # Find wait time of last pool when waiting on multiple pools
            pools = []  # [End Date, index] for each pool in worker pools
            for index, pool in enumerate( workerPool):
                pools.append( [pool.workEnded, index])

            pools.sort( reverse=True)

            if workerPool[ pools[0][1]].poolCreated <= pools[1][0]:
                # First pool created prior to second pool finishing work! We were waiting on multiple pools
                workerPool[ pools[0][1]].waitTime = datetime.datetime.now() - pools[1][0]
                workMsg = ", waited {0} for Pool '{1}'".format( utils._formatTimeDelta( workerPool[ pools[0][1]].waitTime), workerPool[ pools[0][1]].description)
        #

        if showProgress:
            sys.stdout.write( "\r*\n", logging=False)

        sys.stderr.write( "Worker Process Elapsed Time: {0}{1}\n".format( utils._formatTimeDelta( datetime.datetime.now() - start, stripStr=""), waitMsg))

        if workSubmitted - workCompleted:
            sys.stdout.write( u"\n * NOTE * Worker processes terminated before all work was completed!\n")
            return False

        return True

    class _StdOverride( object):
        # Class designed to override sys.stdout and sys.stderr (output) handlers
        def __init__(self, fp, origFp, errFp, logger):
            self._fp = fp
            self._origFp = origFp
            self._errFp = errFp
            self.echo = True
            self.log = True
            self._encoding = getattr(  origFp, "encoding", None)
            self._loggerObject = logger

        @property
        def loggerObject( self):
            return self._loggerObject

        @property
        def encoding( self):
            # Added v1.11.1
            return self._encoding

        @property
        def log( self):
            return self._log

        @log.setter
        def log( self, value):
            # Set to True or False
            self._log = not not value

        @property
        def echo( self):
            return self._echo

        @echo.setter
        def echo( self, value):
            # Set to True or False
            self._echo = not not value

        @property
        def closed( self):
            return getattr( self._origFp, "closed", False)

        def _formatFloat( self, value):
            if value >= 1000.0:
                return "{0:5.0f}".format( value)
            if value >= 100.0:
                return "{0:5.1f}".format( value)
            if value >= 10.0:
                return "{0:5.2f}".format( value)
            else:
                return "{0:5.3f}".format( value)

        def write(self, string, logging=None, echo=None):
            # Allow override of Logging and Echo options
            if logging == None:
                # Get the current property setting
                logging = self.log

            if echo == None:
                # Get the current property setting
                echo = self.echo

            if hasattr( self, "lockObject"):
                self.lockObject.acquire( True)

            if echo:	# Ok to echo to original output?
                if self._origFp and not getattr( self._origFp, "closed", False):
                    try:
                        self._origFp.write( string)
                    except Exception as e:
                        self._origFp.write( " * Failed to write to '{0}': {1}\n".format( getattr( self._origFp, "name", str( self._origFp)), e))

                    try:
                        self._origFp.flush()
                    except:
                        pass

            if logging:	# Ok to log to new output?
                stringList = string.split( "\n")    # Find newlines
                hasNewline = len( stringList) > 1 and not stringList[-1]    # Test if string ends with newline
                if string and self._loggerObject and hasattr( self._loggerObject, "_timestamp"):
                    if self._loggerObject._timestamp and self._loggerObject._showTimestamp:
                        # Inject Timestamp in message, v2.3.0
                        string = ""
                        for index, part in enumerate( stringList):
                            # If string part has content and either last line printed ended with a newline or we are not on the first part
                            #    Add timestamp
                            if part and (self._loggerObject._hadNewline or index):
                                # Validate string part, start after any non-alphanumeric
                                for offset in range( len( part)):
                                    if part[ offset] >= " ":
                                        if not offset:
                                            string += part[0:offset]
                                            part = part[ offset:]
                                        break
                                # Calc Elapsed and Interval times as floating seconds
                                now = datetime.datetime.now()
                                lastTime = now - self._loggerObject._lastTime
                                lastTime = float( "{0}.{1:06d}".format( lastTime.seconds, lastTime.microseconds))
                                self._loggerObject._lastTime = now
                                elapsedTime = self._loggerObject._lastTime - self.loggerObject._startTime
                                elapsedTime = float( "{0}.{1:06d}".format( elapsedTime.seconds, elapsedTime.microseconds))
                                # Alter string if starting on new line, remove trailing zeros in microseconds
                                dateStamp = now.strftime( self.loggerObject._timestamp)
                                dateStamp = dateStamp.replace( "000000", "000") if "000000" in dateStamp else dateStamp.replace( "000", "")
                                dateStamp = dateStamp.replace( "{l}", self._formatFloat( lastTime))
                                string +=   dateStamp.replace( "{e}", self._formatFloat( elapsedTime))
                            if part:
                                # Add string part back in
                                string += part
                            if index < len( stringList) - 1:
                                # Add newline if not last part
                                string += "\n"

                if self._fp and not self._fp.closed:
                    try:
                        if isinstance( string, unicode) and self._encoding:
                            self._fp.write( string.encode( self._encoding))
                        else:
                            self._fp.write( string)

                        if self._loggerObject:
                            #self._loggerObject._hadNewline = string.endswith( "\n")
                            self._loggerObject._hadNewline = hasNewline
                    except Exception as e:
                        self._fp.write( " * Failed to write to LogFile: {0}\n".format( e))

                    try:
                        self._fp.flush()
                    except:
                        pass

                # Echo to Error Log
                if self._errFp and not self._errFp.closed:
                    try:
                        if isinstance( string, unicode) and self._encoding:
                            self._errFp.write( string.encode( self._encoding))
                        else:
                            self._errFp.write( string)
                    except Exception as e:
                        self._errFp.write( " * Failed to write to ErrorLog: {0}\n".format( e))

                    try:
                        self._errFp.flush()
                    except:
                        pass

            if hasattr( self, "lockObject"):
                self.lockObject.release()


        def writelines(self, sequence, logging=None, echo=None):
            if logging == None:
                # Get the current property setting
                logging = self.log

            if echo == None:
                # Get the current property setting
                echo = self.echo

            if hasattr( self, "lockObject"):
                self.lockObject.acquire( True)

            if echo:	# Ok to echo to original output?
                if self._origFp and not getattr( self._origFp, "closed", False):
                    try:
                        self._origFp.writelines( sequence)
                    except Exception as e:
                        self._origFp.write( " * Failed to write to '{0}': {1}\n".format( getattr( self._origFp, "name", str( self._origFp)), e))

                    try:
                        self._origFp.flush()
                    except:
                        pass

            if logging:	# Ok to log to new output?
                if self._fp and not self._fp.closed:
                    try:
                        self._fp.writelines( sequence)
                    except Exception as e:
                        self._fp.write( " * Failed to write to LogFile: {0}\n".format( e))

                    try:
                        self._fp.flush()
                    except:
                        pass

                # Echo to Error Log
                if self._errFp and not self._errFp.closed:
                    try:
                        self._errFp.writelines( sequence)
                    except Exception as e:
                        self._errFp.write( " * Failed to write to ErrorLog: {0}\n".format( e))

                    try:
                        self._errFp.flush()
                    except:
                        pass

            if hasattr( self, "lockObject"):
                self.lockObject.release()

        def flush(self):
            if self._origFp and not getattr( self._origFp, "closed", False):
                try:
                    self._origFp.flush()
                except:
                    pass

#######################################
# Class: _Pool                        #
# Enhanced multiprocessing.Pool class #
#######################################

class _Pool( multiprocessing.pool.Pool):
    """Extend multiprocessing Pool Class to track activity"""

    def __init__( self, processes=None, initializer=None, initargs=(), maxtasksperchild=None):
        self._sumTime = datetime.timedelta( 0)
        self._maxTime = datetime.timedelta( 0)
        self._minTime = datetime.timedelta( 99999999)
        self._idleTime = datetime.timedelta( 0)
        self._poolCreated = datetime.datetime.now()
        self._workStarted = datetime.datetime.now()
        self._workEnded = datetime.datetime.now()
        self._workSubmitted = 0
        self._workCompleted = 0
        self._workSucceeded = 0
        self._workRemaining = 0
        self._lockObject = multiprocessing.Lock()
        self._processes = processes if processes else multiprocessing.cpu_count()

        #return super( _Pool, self).__init__( processes, initializer, initargs, maxtasksperchild)
        if maxtasksperchild:
            # Support for Python v2.7
            return multiprocessing.pool.Pool.__init__( self, processes, initializer, initargs, maxtasksperchild)
        else:
            # Support for Python v2.6
            return multiprocessing.pool.Pool.__init__( self, processes, initializer, initargs)

    def close( self):
        """Close Pool"""

        if not self._workRemaining and self._state != multiprocessing.pool.CLOSE:
            # Set work started to elapsed timedelta
            self._workStarted = datetime.datetime.now() - self._workStarted
            # Add to Idle time if Pool not closed
            self._idleTime += datetime.datetime.now() - self._workEnded

        return multiprocessing.pool.Pool.close( self)

    @property
    def sumTime( self):
        """Return the Summary time of all work performed as a datetime.timedelta"""

        self._lockObject.acquire()
        try:
            return self._sumTime

        finally:
            self._lockObject.release()

    @property
    def idleTime( self):
        """Return the total Idle time of the pool as a datetime.timedelta"""

        self._lockObject.acquire()
        try:
            return self._idleTime

        finally:
            self._lockObject.release()

    @property
    def avgTime( self):
        """Return the Average time of all work performed as a datetime.timedelta"""

        self._lockObject.acquire()
        try:
            if self._workCompleted:
                return self._sumTime / self._workCompleted
            else:
                return datetime.timedelta( 0)

        finally:
            self._lockObject.release()

    @property
    def maxTime( self):
        """Return the Maximum time of all work performed as a datetime.timedelta"""

        self._lockObject.acquire()
        try:
            return self._maxTime

        finally:
            self._lockObject.release()

    @property
    def minTime( self):
        """Return the Minimum time of all work performed as a datetime.timedelta"""

        self._lockObject.acquire()
        try:
            if self._maxTime < self._minTime:
                return datetime.timedelta( 0)
            return self._minTime

        finally:
            self._lockObject.release()

    @property
    def elapsedTime( self):
        """Return the Elapsed time the Pool has been running as a datetime.timedelta"""
        self._lockObject.acquire()
        try:
            if isinstance( self._workStarted, datetime.datetime):
                return datetime.datetime.now() - self._workStarted
            return self._workStarted

        finally:
            self._lockObject.release()

    @property
    def workSubmitted( self):
        """Return the number of work items submitted"""

        self._lockObject.acquire()
        try:
            return self._workSubmitted

        finally:
            self._lockObject.release()

    @property
    def workCompleted( self):
        """Return the number of work items completed"""

        self._lockObject.acquire()
        try:
            return self._workCompleted

        finally:
            self._lockObject.release()

    @property
    def workSucceeded( self):
        """Return the number of work items Successfully completed"""

        self._lockObject.acquire()
        try:
            return self._workSucceeded

        finally:
            self._lockObject.release()

    @property
    def workRemaining( self):
        """Return the number of work items that remain"""

        self._lockObject.acquire()
        try:
            return self._workRemaining

        finally:
            self._lockObject.release()

    @property
    def workEnded( self):
        """Return the datetime of when the Pool finished all work"""

        self._lockObject.acquire()
        try:
            return self._workEnded

        finally:
            self._lockObject.release()

    @property
    def poolCreated( self):
        """Return the datetime of when the Pool was created"""

        self._lockObject.acquire()
        try:
            return self._poolCreated

        finally:
            self._lockObject.release()

    def estimateCompletion( self, asDelta=False):
        """Return the datetime Estimated Completion Time (ECT) for when work will be (or has been) completed"""

        self._lockObject.acquire()
        try:
            # Compute Estimated Completion Time (ECT)
            running = self._processes if self._workRemaining >= self._processes else self._workRemaining

            if running:
                if self._workCompleted:
                    avgTime = self._sumTime / self._workCompleted               # Get average time for all completed work
                    processTime = (datetime.datetime.now() - self._workEnded)   # Get time for current running processes

                    avgTime = avgTime if processTime < avgTime else (processTime + avgTime) / 2 # Use average time completed until processing time is greater than average, then include

                    processStart = self._workEnded                                      # Come as close we can to the start of the current set of processes
                    runsRemaining = int( float( self._workRemaining) / running + 0.5)   # How many multi-processing cycles remain?
                    ect = (processStart + (avgTime * runsRemaining)) - (datetime.datetime.now() if asDelta else datetime.timedelta( seconds=0))  # Return Estimated Time of Completion
                    if isinstance( ect, datetime.timedelta):
                        if ect < datetime.timedelta(0):
                            return datetime.timedelta( 0)
                    elif ect < datetime.datetime.now():
                        return datetime.datetime.now()
                    return ect
                else:
                    return datetime.timedelta( seconds=0) if asDelta else datetime.datetime.now()

            return datetime.timedelta( seconds=0) if asDelta else self._workEnded

        finally:
            self._lockObject.release()

    def _completeWork( self, elapsedTime, success=True):
        """Increment work completed, supplying a timedelta to add to totals"""

        self._lockObject.acquire()
        try:
            self._workCompleted += 1
            self._workEnded = datetime.datetime.now()
            if success:
                self._workSucceeded += 1

            if self._workRemaining:
                self._workRemaining -= 1
                if not self._workRemaining and self._state == multiprocessing.pool.CLOSE:
                    # Set work started to elapsed timedelta
                    self._workStarted = datetime.datetime.now() - self._workStarted

            if isinstance( elapsedTime, datetime.timedelta):
                self._sumTime += elapsedTime
                if elapsedTime > self._maxTime:
                    self._maxTime = elapsedTime
                if elapsedTime < self._minTime:
                    self._minTime = elapsedTime
        finally:
            self._lockObject.release()

    def _incrementWork( self):
        """Increment work submitted"""

        self._lockObject.acquire()
        try:
            #if not self._workSubmitted:
            #    # Initialize work start time
            #    self._workStarted = datetime.datetime.now()
            if not self._workRemaining:
                # Add to Idle time, last end time minus now. v2.3.0
                self._idleTime += datetime.datetime.now() - self._workEnded
            self._workSubmitted += 1
            self._workRemaining += 1

        finally:
            self._lockObject.release()

    def map(self, func, iterable, chunksize=None):
        """Not implemented"""
        raise Exception( "'map' function NOT implemented yet")
        #self._incrementWork()
        #return multiprocessing.pool.Pool.map(self, func, iterable, chunksize)

    def imap(self, func, iterable, chunksize=1):
        """Not implemented"""
        raise Exception( "'imap' function NOT implemented yet")
        #self._incrementWork()
        #return multiprocessing.pool.Pool.imap(self, func, iterable, chunksize)

    def imap_unordered(self, func, iterable, chunksize=1):
        """Not implemented"""
        raise Exception( "'imap_unordered' function NOT implemented yet")
        #self._incrementWork()
        #return multiprocessing.pool.Pool.imap_unordered(self, func, iterable, chunksize)

    def apply_async(self, func, args=(), kwds={}, callback=None):
        self._incrementWork()

        if not kwds:
            # Make sure it's a Dictionary
            kwds = {}

        if not isinstance( kwds, dict):
            raise Exception( "Invalid Keywords (kwds) argument: Not a Dictionary")

        return multiprocessing.pool.Pool.apply_async(self, _asyncFunction, [func, args, kwds, callback], callback=self._callback)

    def map_async(self, func, iterable, chunksize=None, callback=None):
        """Not implemented"""
        raise Exception( "'map_async' function NOT implemented yet")
        #self._incrementWork()
        #return multiprocessing.pool.Pool.map_async(self, func, iterable, chunksize, callback)

    def _callback( self, results):
        # Extract arguments from results
        pid, taskid, function, elapsedTime, args = results
        success = False
        cleanExit = False

        # Check for error passed back, function is PID and args is Exception
        if isinstance( function, int):
            sys.stdout.write("\n * Worker pid-{0}, task-{1} encountered an Unhandled Exception: '{2}'\n".format( pid, taskid, args))
            sys.stdout.loggerObject._exitValue = "Multiprocessing Error"
            self._completeWork( elapsedTime, success)
        else:
            try:
                if function and callable( function):
                    function( *args)
                success = True
                cleanExit = True

            except Exception as e:
                sys.stdout.write( "\n * Worker pid-{0}, task-{1} encountered Error during Async-callback: '{2}'\n".format( pid, taskid, e))
                traceback.print_exc()
                sys.stdout.loggerObject._exitValue = "Multiprocessing Error"
                cleanExit = True

            finally:
                self._completeWork( elapsedTime, success)
                if not cleanExit:
                    sys.stdout.write(
                        "\n * Detected premature exit of callback thread by Worker pid-{0}, task-{1} *"
                        "\n   Subsequent Callback operations and statistical updates{2} are ignored!\n".format( pid, taskid,
                        "" if not hasattr( self, "description") else " for Pool '{0}'".format( self.description)))

##########################################################
# Initialize Work Pool Process                           #
#                                                        #
# Internal function used by Logger class to initialize   #
# Worker process and setup Log file management.          #
#                                                        #
# Function needs to reside outside of Logger Class to    #
# allow proper Process instantiation.                    #
##########################################################

def _initWorkerPool( logFilename, description, timestamp, function, args):
    """Internal function, not intended for general consumption!"""
    global ALFlog, PoolProcessTimer, pid, initialized, taskid

    PoolProcessTimer = StopWatch()
    pid = multiprocessing.current_process().pid
    name = multiprocessing.current_process().name
    initialized = False
    taskid = 0

    logfile = os.path.splitext( logFilename)
    logfile = logfile[0] + "_wpID-{0}".format( pid) + logfile[1]

    _logFP = sys.stdout

    try:
        _logFP = open( logfile, "w")
    except Exception as e:
        print( "\n * Unable to create Worker log '{0}', error: {1}\n".format( logfile, e))

    if "ALFlog" not in globals():
        ALFlog = utils.dummyLogger()

    sys.stdout = utils.Logger._StdOverride( _logFP, sys.stdout, None, ALFlog)
    sys.stdout.echo = False
    utils.stdout = sys.stdout   # Added v1.9.2
    sys.stderr = utils.Logger._StdOverride( _logFP, sys.stderr, None, ALFlog)
    sys.stderr.echo = False
    utils.stderr = sys.stderr   # Added v1.9.2

    print( "\nInitializing '{0}' worker pool process: pid-{1} ({2}), {3}".format( description, pid, name, datetime.datetime.now().strftime( '%H:%M:%S %a %m/%d/%Y')))

    # Invoke User-supplied initialization function if defined
    if function:
        try:
            if callable( function) and not function.__name__.startswith( "_"):
                # Report function being called (as long as it's not an internal function)
                print( "\nCalling function: '{0}'...".format( function.__name__))

            # Set Timestamp
            ALFlog.timestamp = timestamp

            function( *args)
            initialized = True

        except Exception as e:
            print( "\n * Failed to execute User-Defined Initialization: '{0}'\n".format( e))
            # Turn Timestamp off
            ALFlog.showTimestamp = False
            traceback.print_exc()
    else:
            initialized = True

    # Turn Timestamp on
    ALFlog.showTimestamp = True

def _asyncFunction( function, args, kwds, callback):
    """Internal function, not intended for general consumption!"""
    global ALFlog, PoolProcessTimer, pid, initialized, taskid

    # Turn Timestamp off
    ALFlog.showTimestamp = False

    taskid += 1
    print( "\n######## Starting Async task-{0} at {1} ########".format( taskid, datetime.datetime.now().strftime( '%H:%M:%S %a %m/%d/%Y')))

    PoolProcessTimer.start()

    try:
        if not initialized:
            msg = "Worker process failed to Initialize"
            print( "\n * {0} *".format( msg))
            raise utils.InitializationError( msg)

        if callable( function) and not function.__name__.startswith( "_"):
            # Report function being called (as long as it's not an internal function)
            print( "\nCalling function: '{0}'...".format( function.__name__))

        # Turn Timestamp on
        ALFlog.showTimestamp = True

        result = function( *args, **kwds)

        # Turn Timestamp off
        ALFlog.showTimestamp = False

        # Check and restructure result when successful
        if result is None:
            # Nothing returned! Make the result an empty Tuple!
            result = ()
        elif not isinstance( result, tuple):
            # Make it a Singleton Tuple!
            result = ( result,)

    except Exception as e:
        # Set Callback action to Process ID and report error!
        callback = pid
        result = e
        if not isinstance( e, utils.InitializationError):
            print( "\n * Failed to execute User-Defined Function *\n")
            # Turn Timestamp off
            ALFlog.showTimestamp = False
            traceback.print_exc()

    elapsedTime = PoolProcessTimer.stop()

    print( "\nTask Elapsed Time: {0}".format( utils._formatTimeDelta( elapsedTime, stripStr="")))

    # Turn Timestamp on
    ALFlog.showTimestamp = True

    return pid, taskid, callback, elapsedTime, result

def _formatTimeDelta( delta, decPlaces=2, stripStr="0:", verbose=False):
    """Internal function, not intended for general consumption!"""
    if isinstance( delta, datetime.timedelta):
        if not decPlaces:
            decPlaces = 0
        elif not isinstance( decPlaces, int) and not isinstance( decPlaces, long):
            decPlaces = 2

        if decPlaces < 0:
            decPlaces = abs( decPlaces)

        if not stripStr:
            stripStr = ""
        elif not isinstance( stripStr, basestring):
            stripStr = "0:"

        seconds = round( float( delta.microseconds) / 10**6 + delta.days * 86400 + delta.seconds, decPlaces)

        delta = str( datetime.timedelta( seconds=int( seconds))).lstrip( stripStr)
        delta = "{0}{1}".format( delta if delta else 0, os.path.splitext( "{0:.{1}f}".format( seconds, decPlaces))[1])

        if " " in delta:
            # Has Days, compact to 'days:hrs:mins:secs"...
            delta = delta.split()
            delta = ":".join( [delta[0], delta[-1]])

        if verbose:
            delta = delta.split( ":")
            output = ""
            textSingle = ["day, ", "hr, ", "min, ", "sec"]
            textPlural = ["days, ", "hrs, ", "mins, ", "secs"]
            for index in range( -1, -(len( delta)+1), -1):
                # Skip if value is zero, unless it is seconds
                if index == -1 or not delta[ index] in ["0", "00"]:
                    if delta[ index][0] == "0" and len( delta[ index].split( ".")[0]) > 1:
                        # Trim leading zero if has more than one integer digit
                        delta[ index] = delta[ index][1:]
                    output = "{0} {1}{2}".format( delta[ index], textSingle[ index] if delta[ index] == "1" else textPlural[ index], output)
            return output
        else:
            return delta

    return str( delta)

class dummyLogger( object):
    """Class: dummyLogger()

    Provides 'function' compatability with the Logger class. Allowing existing
    logic to leverage Logger function calls from both a single or a multi-
    processing configuration without requiring code changes.

    All log output is simply displayed to sys.stdout.

    Use this class during multi-process initialization to create a matching
    Logger object, one that is named the same as the Logger object used to
    create your worker pool.
"""
    def __init__( self):
        self._exitValue = False
        self._keepActivity = False
        self._timestamp = ""
        self._showTimestamp = True
        # Standard Override properties
        self._startTime = datetime.datetime.now()
        self._lastTime = self._startTime
        self._hadNewline= True

    def close( self):
        pass

    @property
    def keepActivity( self):
        return self._keepActivity

    @keepActivity.setter
    def keepActivity( self, value):
        if type( value) == type( True):
            self._keepActivity = value

    @property
    def timestamp( self):
        return self._timestamp

    @timestamp.setter
    def timestamp( self, mask):
        if mask and isinstance( mask, basestring):
            try:
                if datetime.datetime.now().strftime( mask):
                    self._timestamp = mask
            except Exception as e:
                sys.stderr.write( " * Failed to set ALFlog timestamp to '{0}': {1}\n".format( mask, e))
        else:
            self._timestamp = ""

    @property
    def showTimestamp( self):
        return self._showTimestamp

    @showTimestamp.setter
    def showTimestamp( self, enable):
        self._showTimestamp = True if enable else False

    def archive( self, message, echo=False):
        print( "Archive message: {0}".format( message))

    def log( self, message):
        print( message)

    def resetError( self):
        self._exitValue = False

    def setError( self, value):
        self._exitValue = value

    def createWorkerPool( self, initFunction="", args=[], description="", processCount=0):
        print( "dummyLogger object does not support 'createWorkerPool' operation!")

############################################################
# AppLock                                                  #
#                                                          #
# Code Source: http://code.activestate.com/recipes/576891/ #
#          By: Max Polk - MIT, Aug 2009                    #
#                                                          #
# Build: v1.0.1, April 2015, Paul Dodd - esri              #
#     - Added Try block to 'unlock' function close logic.  #
#     - Added
# Build: v1.0.0, May 2012, Paul Dodd - esri                #
#     - Augmented to support Windows                       #
############################################################

class AppLock( object):
    """Class: AppLock( <lockFile>)

    Ensures application is running only once by creating a lock file.

    Ensure call to lock is True. Then call unlock at exit to remove
    lock file.

    Where:
        <lockFile> = (required) Path and Name of file to create for lock.

    Methods:
          '<object>.lock()' Place lock on file. Return True if successful
                            or False if not (another instance has the file).
        '<object>.unlock( [<tries>[, <wait>]])' Remove lock placed on file.

    Remarks:
        You cannot read or write to the lock file, but for some reason
        you can remove it.  Once removed, it is still in a locked state
        somehow.  Another application attempting to lock against the file
        will fail, even though the directory listing does not show the
        file.  Mysterious, but we are glad the lock integrity is upheld
        in such a case.

    Instance variables:
        lockfile  -- Full path to lock file
        lockfd    -- File descriptor of lock file exclusively locked
"""

    def __init__( self, lockfile):
        self.lockfile = lockfile
        self.lockfd = None

    def lock( self):
        """Method: lock()

    Creates and holds on to the lock file with exclusive access.

    Returns:
        True if lock successful, False if otherwise. An exception is raised
        if operating system errors encountered while creating the lock file.
"""

        try:
            import fcntl
            self._windows = False
        except:
            self._windows = True

        try:
            #
            # Create or else open and trucate lock file, in read-write mode.
            #
            # A crashed app might not delete the lock file, so the
            # os.O_CREAT | os.O_EXCL combination that guarantees
            # atomic create isn't useful here.  That is, we don't want to
            # fail locking just because the file exists.
            #
            # Could use os.O_EXLOCK, but that doesn't exist yet in my Python
            #
            if self._windows and os.access( self.lockfile, os.F_OK):
                os.remove( self.lockfile)	# Should fail if in use!

            self.lockfd = os.open (self.lockfile,
                os.O_TRUNC | os.O_CREAT | os.O_RDWR)

            if not self._windows:
                # Acquire exclusive lock on the file, but don't block waiting for it
                fcntl.flock (self.lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)

                # Writing to file is pointless, nobody can see it
                os.write (self.lockfd, "My Lockfile")

            return True

        except (OSError, IOError), e:
            # Lock cannot be acquired is okay, everything else reraise exception
            if e.errno in (errno.EACCES, errno.EAGAIN):
                return False
            else:
                raise

    def unlock( self, tries=3, wait=5):
        """Method: Unlock( [<tries>[, <wait>]])

    Release File Lock and delete lock file.

    Where:
        <tries> = (optional) Number of attempts that can be made to free lock.
                  Default is 3
         <wait> = (optional) Number of seconds to wait between attempts.
                  Default is 5

    Returns:
        None on success or String with text details on retry/failure progress.
"""
        def closeIt():
            try:
                os.close( self.lockfd)

            except:
                pass

        outcome = ""

        # FIRST unlink file, then close it.  This way, we avoid file
        # existence in an unlocked state. Except for Windows, need to close first!
        if self._windows:
            # v1.0.1, added additional try block to ignore any issues on first close!
            closeIt()

        for attempt in range( 1, tries + 1):
            try:
                os.unlink( self.lockfile)
                if attempt > 1:
                    outcome += "\n - Lock released on attempt {0}!".format( attempt)
                break

            except Exception as e:
                outcome += "\n * Unlock attempt {0} of {1} Failed: {2}".format( attempt, tries, e)

            if attempt != tries:
                time.sleep( wait)
        else:
            outcome += "\n * Failed to release lock file!"

        # Just in case, let's not leak file descriptors
        closeIt()

        return (outcome if outcome else None)

####################################################
# Generic stub class providing common data Caching #
# features for data specific to other Classes.     #
#                                                  #
# Maintains a sorted List of Dictionary items.     #
#                                                  #
# Output: Local cache file updated once daily.     #
#         Cache file stored in System Temp folder. #
#                                                  #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri        #
#     - Restructured code to better adhere to      #
#       Python standards and best practices.       #
# Build: v1.0.0, Feb 2012, Paul Dodd - esri        #
####################################################

class _CacheLoader( object):
    """Internal function, not intended for general consumption!"""
    # Test Cache file to see if it needs to be reloaded, True if modified date of file is not today
    def loadRequired( self):
        # Check existance of Cached content
        if os.access( self.fileName, os.R_OK):
            fromtimestamp = datetime.date.fromtimestamp
            today = time.time()

            # Check if refresh required
            if fromtimestamp( os.stat( self.fileName).st_mtime) == fromtimestamp( today):
                return False

        return True

    # Download and save URL content to file
    def _download( self, url, fileName):
        iFP = urllib2.urlopen( url)
        oFP = open( fileName, 'w')

        line = iFP.readline()
        while line:
            oFP.write( line)
            line = iFP.readline()

        iFP.close()
        oFP.close()

    def loadData( self):
        fileName = self.fileName
        fileNameOld = fileName + '.old'
        url = self.dataSource

        try:
            # Need to Download new content?
            if self.loadRequired():
                # Save existing file
                if os.access( fileName, os.F_OK):
                    if os.access( fileNameOld, os.F_OK):
                        os.remove( fileNameOld)
                    os.rename( fileName, fileNameOld)

                try:
                    # Yes, download!
                    self._download( url, fileName)

                except Exception as e:
                    if hasattr( self, 'dataAlternate'):
                        # Try Alternate data source if exist
                        sys.stderr.write( "\n * Using Alternate data source * Failed to load Primary from:\n   '{0}',\n   {1}\n".format( url, e))
                        url = self.dataAlternate
                        self._download( url, fileName)
                    else:
                        raise e

            # Clear List and Dict
            self.itemList = []
            self.itemDict.clear()

            # Return open file handle
            return open( fileName, 'rt')

        except Exception as e:

            # Check for old copy of cached file
            if os.access( fileNameOld, os.F_OK):
                # Clear current cache file if exists
                if os.access( fileName, os.F_OK):
                    os.remove( fileName)

                # Restore old copy
                os.rename( fileNameOld, fileName)
                sys.stderr.write( "\n * Using Fallback Cache * Failure in Cache 'loadData' routine, cannot update from:\n   '{0}',\n   {1}\n".format( url, e))

                # Return open file handle
                return open( fileName, 'rt')
            else:
                raise Exception( " * Failure in Cache 'loadData' routine, cannot update from:\n  '{0}',\n   {1}".format( url, e))

    # Add item to ordered Dictionary cache
    def _addData( self, key, value):
        if key not in self.itemDict:
            # Add key to ordered list
            self.itemList.append( key)

        # Add item to indexed list
        self.itemDict[ key] = value

        # Return item
        return self.itemDict[ key]

    # Sort data
    def _sortData( self):
        self.itemList.sort()

    # Report if item is in Dictionary cache
    def __contains__( self, item):
        return (item in self.itemDict)

    # Get item or indexed item from Dictionary cache
    def __getitem__( self, item):
        if isinstance( item, int) or isinstance( item, long):
            if item < 0 or item >= len( self.itemList):
                raise IndexError( item)
            else:
                return self.itemDict[ self.itemList[ item]]

        if not item in self.itemDict:
            raise KeyError( item)
        else:
            return self.itemDict[ item]

    # Return number of items in Dictionary cache
    def __len__( self):
        return len( self.itemList)

    # Initialize, specifying name of file to maintain
    def __init__( self, fileName):
        scriptName = os.path.split( __file__)[-1]

        # Set Cache filename to system temp storage location + script name + fileName
        self.fileName = os.path.join( tempfile.gettempdir(), "{0}_{1}".format( scriptName.split( ".")[0], fileName))

        # Setup Dictionary cache storage
        self.itemList = []
        self.itemDict = {}

####################################################################
# Load Country Code/Description cross reference data. Maintains an #
# internal List sorting items by selected 'indexOn' field order.   #
#                                                                  #
# Source:                                                          #
# http://ftp.univie.ac.at/netinfo/iso/iso3166-countrycodes.txt     #
# (alt) Product Maint: ftp://ftp.ripe.net/iso3166-countrycodes.txt #
# (old)  ftp://ftp.fu-berlin.de/doc/iso/iso3166-countrycodes.txt   #
#                                                                  #
# Data Dict cache: <countryName>, <abbr2>, <abbr3>, <countryCode>  #
#                                                                  #
# 'indexOn' property controls which data Field to index Dict on    #
#     (default) None = Do not initially load data                  #
#                  1 = Country code                                #
#                  2 = 2-digit abbreviation                        #
#                  3 = 3-digit abbreviation                        #
#                                                                  #
# Build: v1.0.2, Aug 2013, Paul Dodd - esri                        #
#     - Added alternate source                                     #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri                        #
#     - Restructured code to better adhere to Python standards and #
#       best practices.                                            #
# Build: v1.0.0, Feb 2012, Paul Dodd - esri                        #
####################################################################

class CountryCodeLoader( _CacheLoader):

    """Class: CountryCodeLoader( [<indexOn>])

    Initialize new <object> and load Country Name cross reference data,
    ordering items by desired field index.

    Where <indexOn> (optional) can be:
        (default) None = Init only, do not load data. Must manually
                         invoke 'loadData' method to initiate data load.
                     1 = Index items by Country Code field
                     2 = Index items by 2-digit abbreviation field
                     3 = Index items by 3-digit abbreviation field

    Dictionary items are stored in the form of:
        {'Name': 'UNITED STATES', 'Code': '840', 'Abbr2': 'US', 'Abbr3': 'USA'}

    Methods:
        '<object>.loadData( <indexOn>)' Sets field index and loads data, or
                                        re-indexes data if already loaded.
        '<object>.loadRequired()' Returns True if data load has not been done
                                  or if data has not been refreshed today.

    Properties:
        '<object>.fileName' Get name of cache file.
        '<object>.dataSource' Get URL source of data.
        '<object>.indexOn' Get or Sets field index value.

    Data lookup:
        '<object>[ <index>]' Where <index> = 0 to 'len( <object>)' - 1
        '<object>[ <str>]' Where <str> = value related to index field chosen.

    Use: 'if <str> in <object>' to query existance of a specific item.
         'for item in <object>' to iterate through indexed content.
         'len( <object>)' to query for total number of items.
"""

    def __init__( self, indexOn=None):
        # Init base
        super( CountryCodeLoader, self).__init__( "CountryXref.txt")

        # Set URL Source location of data
        self.dataSource = "http://ftp.univie.ac.at/netinfo/iso/iso3166-countrycodes.txt"
        self.dataAlternate = "ftp://ftp.ripe.net/iso3166-countrycodes.txt"

        # Set indexing
        self.indexOn = indexOn

        # Load if index is not None
        if indexOn:
            self.loadData()

    def loadData( self, indexOn=None):
        try:
            if indexOn:
                self.indexOn = indexOn
            else:
                indexOn = self.indexOn

            # Initiate common download logic, returning file handler
            iFP = super( CountryCodeLoader, self).loadData()

            # Parse data if index has been set
            if indexOn:
                # Reset value to word index of incoming data rows
                indexOn -= 1
                if indexOn == 0:
                    indexOn = 3

                # Setup flags
                line = " "
                start = False

                # Start reading data
                while line:
                    line = iFP.readline()

                    # Has to be greater than 9 characters, 1+2+3+3 minimum for all fields
                    if len(line) > 9:
                        if line[0] == '-':
                            start = True
                        elif start:
                            rowData = line.rsplit( None, 3)

                            # Add data ( Key, Value)
                            self._addData( rowData[ indexOn], {
                                "Name": rowData[0],
                                "Abbr2": rowData[1],
                                "Abbr3": rowData[2],
                                "Code": rowData[3]
                            })

                self._sortData()

            iFP.close()

        except Exception as e:
            raise Exception( " * Error Loading Country Codes: {0}".format( e))

    @property
    def indexOn( self):
        return self._indexOn

    @indexOn.setter
    def indexOn( self, value):
        # Verify property value
        if not (value == None or isinstance( value, int)):
            raise TypeError( "Invalid data Type '{0}'!".format( type( value)))

        if value and (value < 1 or value > 3):
            raise AttributeError( "Value out of Range!")

        self._indexOn = value

####################################################################
# Load Weather Station reference data. Maintains an internal List  #
# sorting items by selected 'indexOn' field order.                 #
#                                                                  #
# Source:                                                          #
# http://www.aviationweather.gov/static/adds/metars/stations.txt   #
# (alt) http://weather.rap.ucar.edu/surface/stations.txt           #
#                                                                  #
# 'indexOn' property controls which data Field to index Dict on.   #
#     (default) None = Do not initially load cache                 #
#                  1 = ICAO international ID                       #
#                  2 = IATA (FAA) ID                               #
#                  3 = SYNOP international ID number               #
#                                                                  #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri                        #
#     - Restructured code to better adhere to Python standards and #
#       best practices.                                            #
# Build: v1.0.0, Feb 2012, Paul Dodd - esri, Technical Marketing   #
####################################################################

class WeatherStationLoader( _CacheLoader):

    """Class: WeatherStationLoader( [<indexOn>])

    Initialize new <object> and load Weather Station reference data,
    ordering items by desired field index.

    Where <indexOn> (optional) can be:
        (default) None = Init only, do not load data. Must manually
                         invoke 'loadData' method to initiate data load.
                     1 = Index items by ICAO international ID field
                     2 = Index items by IATA (FAA) ID field
                     3 = Index items by SYNOP international ID field

    Dictionary items are stored in the form of:
        {'Name': 'JACKSONVILLE', 'Province': 'FLORIDA', 'Country':
         'UNITED STATES', 'ICAO': 'KJAX', 'IATA': 'JAX', 'SYNOP': 72206,
         'Longitude': -81.6833333337, 'Latitude': 30.5, 'Elevation': '10m',
         'LastUpdated': '10-FEB-12', 'PlotPriority': 0

         * Note * If attribute flags are present, item may also include:

         'Mflag': <char> if 'M' flag value unknown, or
             'METAR': True
         'Nflag': <char> if 'N' flag value unknown, or
             'NEXRAD': True
         'Vflag': <char> if 'V' flag value unknown, or
             'AIRMET': True, 'SIGMET': True, 'ARTCC': True, 'TAF': True
         'Uflag': <char> if 'U' flag value unknown, or
             'RAWINSONDE': True, 'WINDPROFILER': True
         'Aflag': <char> if 'A' flag value unknown, or
             'ASOS': True, 'AWOS': True, 'MESO': True,
             'HUMAN': True, 'AUGMENTED': True
         'Cflag': <char> if 'C' flag value unknown, or
             'WFO': True, 'RFC': True, 'NCEP': True
        }

    Methods:
        '<object>.loadData( <indexOn>)' Sets field index and loads data, or
                                        re-indexes data if already loaded.
        '<object>.loadRequired()' Returns True if data load has not been done
                                  or if data has not been refreshed today.

    Properties:
        '<object>.fileName' Get name of cache file.
        '<object>.dataSource' Get URL source of data.
        '<object>.indexOn' Get or Sets field index value.

    Data lookup:
        '<object>[ <index>]' Where <index> = 0 to 'len( <object>)' - 1
        '<object>[ <str>]' Where <str> = value related to index field chosen.

    Use: 'if <str> in <object>' to query existance of a specific item.
         'for item in <object>' to iterate through indexed content.
         'len( <object>)' to query for total number of items.
"""

    def __init__( self, indexOn=None):
        # Init base
        super( WeatherStationLoader, self).__init__( "StationXref.txt")

        # Set URL to Source location of data
        self.dataSource = "http://www.aviationweather.gov/static/adds/metars/stations.txt"
        self.dataAlternate = "http://weather.rap.ucar.edu/surface/stations.txt"
        # old alt: "http://www.rap.ucar.edu/weather/surface/stations.txt"

        # Set indexing
        self.indexOn = indexOn

        # Load Country Xref
        self.countryCodes = CountryCodeLoader(2)

        # Load if index is not None
        if indexOn:
            self.loadData()

    def loadData( self, indexOn=None):
        try:
            if indexOn:
                self.indexOn = indexOn
            else:
                indexOn = self.indexOn

            # Initiate common download logic, returning file handler
            iFP = super( WeatherStationLoader, self).loadData()

            # Parse data if index has been set
            if indexOn:
                # Reset value to word index of incoming data rows
                indexOn += 1

                # Setup flags
                line = " "
                lastCountry = "" # Could be State/Province/ or Country name
                lastUpdated = "" # Last date content was updated as: DD-MMM-YY

                # Start reading data
                while line:
                    line = iFP.readline()

                    # Has to be greater than 9 characters, minimum field length
                    if (len(line) > 10) and not (line.startswith( '!') or line.startswith( 'CD  STATION')):
                        if len(line) < 84:
                            newCountry = line.rsplit(None, 1)

                            if newCountry[1].count('-') == 2:
                                # State/Province/or Country record
                                lastCountry = newCountry[0]
                                lastUpdated = newCountry[1]
                        else:
                            # Station record
                            rowData = [
                                line[  0:2].strip(), # CD = 2 letter state (province) abbreviation
                                line[ 3:19].strip(), # STATION = 16 character station long name
                                line[20:24].strip(), # ICAO = 4-character international id
                                line[26:29].strip(), # IATA = 3-character (FAA) id
                                self.toInt(line[32:37]), # SYNOP = 5-digit international synoptic number
                                utils.dms2dd( degrees=line[39:41], minutes=line[42:44], seconds=None, bearing=line[44]), # LAT = Latitude (degrees minutes)
                                utils.dms2dd( degrees=line[47:50], minutes=line[51:53], seconds=None, bearing=line[53]), # LON = Longitude (degree minutes)
                                self.toInt(line[55:59]), # ELEV = Station elevation (meters)
                                line[   62].strip(), # M = METAR reporting station.   Also Z=obsolete? site
                                line[   65].strip(), # N = NEXRAD (WSR-88D) Radar site
                                line[   68].strip(), # V = Aviation-specific flag (V=AIRMET/SIGMET end point, A=ARTCC T=TAF U=T+V)
                                line[   71].strip(), # U = Upper air (rawinsonde=X) or Wind Profiler (W) site
                                line[   74].strip(), # A = Auto (A=ASOS, W=AWOS, M=Meso, H=Human, G=Augmented) (H/G not yet impl.)
                                line[   77].strip(), # C = Office type F=WFO/R=RFC/C=NCEP Center
                                self.toInt(line[79]),# Digit that follows is a priority for plotting (0=highest)
                                line[81:83].strip()  # Country code (2-char) is last column
                            ]

                            if rowData[ indexOn]: # Ignore rows with null index field values
                                # Update elevation
                                if rowData[7]:
                                    rowData[7] = "{0}m".format( rowData[7])

                                # Add data ( Key, Value) and complete field updates
                                newItem = self._addData( rowData[ indexOn], {
                                    "LastUpdated": lastUpdated,
                                    "Name": rowData[1],
                                    "ICAO": rowData[2],
                                    "IATA": rowData[3],
                                    "SYNOP": rowData[4],
                                    "Latitude": rowData[5],
                                    "Longitude": rowData[6],
                                    "Elevation": rowData[7],
                                    "PlotPriority": rowData[14]
                                })

                                # Add province and country
                                if rowData[15] and rowData[15] in self.countryCodes:
                                    # Country code exists, use it
                                    newItem['Country'] = self.countryCodes[ rowData[15]]['Name']

                                    # Set province
                                    if lastCountry != newItem['Country']:
                                        newItem['Province'] = lastCountry
                                    else:
                                        newItem['Province'] = None
                                else:
                                    # No country code, use last
                                    newItem['Country'] = lastCountry
                                    newItem['Province'] = None

                                # M = METAR reporting station.   Also Z=obsolete? site
                                if rowData[8] and rowData[8] != 'Z':
                                    if rowData[8] == 'X':
                                        newItem['METAR'] = True
                                    else:
                                        newItem['Mflag'] = rowData[8]

                                # N = NEXRAD (WSR-88D) Radar site
                                if rowData[9] and rowData[9] != 'Z':
                                    if rowData[9] == 'X':
                                        newItem['NEXRAD'] = True
                                    else:
                                        newItem['Nflag'] = rowData[9]

                                # V = Aviation-specific flag (V=AIRMET/SIGMET end point, A=ARTCC T=TAF U=T+V)
                                if rowData[10] and rowData[10] != 'Z':
                                    if rowData[10] == 'T':
                                        newItem['TAF'] = True
                                    elif rowData[10] == 'U':
                                        newItem['AIRMET'] = True
                                        newItem['SIGMET'] = True
                                        newItem['TAF'] = True
                                    elif rowData[10] == 'V':
                                        newItem['AIRMET'] = True
                                        newItem['SIGMET'] = True
                                    elif rowData[10] == 'A':
                                        newItem['ARTCC'] = True
                                    else:
                                        newItem['Vflag'] = rowData[10]

                                # U = Upper air (rawinsonde=X) or Wind Profiler (W) site
                                if rowData[11] and rowData[11] != 'Z':
                                    if rowData[11] == 'X':
                                        newItem['RAWINSONDE'] = True
                                    elif rowData[11] == 'W':
                                        newItem['WINDPROFILER'] = True
                                    else:
                                        newItem['Uflag'] = rowData[11]

                                # A = Auto (A=ASOS, W=AWOS, M=Meso, H=Human, G=Augmented) (H/G not yet impl.)
                                if rowData[12] and rowData[12] != 'Z':
                                    if rowData[12] == 'A':
                                        newItem['ASOS'] = True
                                    elif rowData[12] == 'W':
                                        newItem['AWOS'] = True
                                    elif rowData[12] == 'M':
                                        newItem['MESO'] = True
                                    elif rowData[12] == 'H':
                                        newItem['HUMAN'] = True
                                    elif rowData[12] == 'G':
                                        newItem['AUGMENTED'] = True
                                    else:
                                        newItem['Aflag'] = rowData[12]

                                # C = Office type F=WFO/R=RFC/C=NCEP Center
                                if rowData[13] and rowData[13] != 'Z':
                                    if rowData[13] == 'F':
                                        newItem['WFO'] = True
                                    elif rowData[13] == 'R':
                                        newItem['RFC'] = True
                                    elif rowData[13] == 'C':
                                        newItem['NCEP'] = True
                                    else:
                                        newItem['Cflag'] = rowData[13]

                # Sort list
                self._sortData()

            iFP.close()

        #except Exception as e:
        except IOError as e:
            raise Exception( " * Error Loading Weather Stations: {0}".format( e))

    def toInt( self, value):
        if value and value.strip().isdigit():
            return int( value)
        return None

    @property
    def indexOn( self):
        return self._indexOn

    @indexOn.setter
    def indexOn( self, value):
        # Verify property value
        if not (value == None or isinstance( value, int)):
            raise TypeError( "Invalid data Type '{0}'!".format( type( value)))

        if value and (value < 1 or value > 3):
            raise AttributeError( "Value out of Range!")

        self._indexOn = value

#########################################################
# OrderedDict, stop-gap before transition to Python 2.7 #
#                                                       #
# Maintains an Ordered Dictionary of key/value pairs.   #
#                                                       #
# Build: v1.1.0, Apr 2014, Paul Dodd - esri             #
#     - Added 'repr' override method to support object  #
#       content explorartion.                           #
# Build: v1.0.0, Jun 2012, Paul Dodd - esri             #
#########################################################

class OrderedDict( object):
    """Class: OrderedDict()

    Creates an Ordered Dictionary that maintains order of insertion for
    Key/Value pairs.

    Methods:
        '<object>.add( key, value)' Add Key/Value pair to dictionary.
        '<object>.iterkeys()'       Return iterable list of Keys.
        '<object>.iteritems()'      Return iterable list of key and value
                                    pairs.

    Data lookup:
        '<object>[ <index>]' Return Value for Key at given index.
                             Where <index> = 0 to 'len( <object>)' - 1.
        '<object>[ <key>]'   Return Value for given Key.
        '<object.<key>'      Return Value for given Key.

    Data assignment:
        '<object>[ <index>] = <value>' Set Value for Key at given index.
                             Where <index> = 0 to 'len( <object>)' - 1.
        '<object>[ <key>] = <value>'   Add Key/Value or Set Value for
                                       given Key.

    Use: 'if <key> in <object>' to query existance of a specific Key.
         'for item in <object>' to iterate values for ordered content.
         'len( <object>)' to query for total number of items.
"""

    def __init__( self):
        self._collection = []

    # Return number of items in the collection
    def __len__( self):
        return len( self._collection)

    # Return indexed item from collection by order
    def __getitem__( self, item):
        if isinstance( item, int) or isinstance( item, long):
            if item < 0 or item >= len( self._collection):
                raise IndexError( item)
            else:
                return getattr( self, self._collection[ item])

        if not hasattr( self, item):
            raise KeyError( item)
        else:
            return getattr( self, item)

    # Set item, by index or name
    def __setitem__( self, item, value):
        if isinstance( item, int) or isinstance( item, long):
            if item < 0 or item >= len( self._collection):
                raise IndexError( item)
            else:
                setattr( self, self._collection[ item], value)
        else:
            if not hasattr( self, item):
                self.add( item, value)
            else:
                return setattr( self, item, value)

    # Report if key is in collection
    def __contains__( self, key):
        return hasattr( self, key)

    # Return formal String representation
    def __repr__( self):
        result = ""
        utils._OrderedDictTabs = getattr( utils, "_OrderedDictTabs", 0) + 1
        for key in self._collection:
            if result:
                result += ","
            result += "\n" + "\t" * utils._OrderedDictTabs + "{0}: {1}".format( repr( key), repr( self[key]))

        utils._OrderedDictTabs -= 1
        if result:
            result += "\n" + "\t" * utils._OrderedDictTabs
        return "{" + result + "}"

    # Iter through Keys
    def iterkeys( self):
        return iter(self._collection)

    # Iter through Key, Value pairs
    def iteritems( self):
        for key in self._collection:
            yield key, getattr( self, key)

    # Add item to collection
    def add( self, key, value):
        if not hasattr( self, key):
            self._collection.append( key)
            setattr( self, key, value)

###################################################
# Display single line Progress message to console #
#                                                 #
# Build: v1.0.0, Jul 2012, Paul Dodd - esri       #
###################################################

class Progress( object):
    """Class: Progress( [<interval>, [<verbose>]])

    Manage message display to console as Progress. Only display a message
    once every <interval>. Will not 'Log' message if 'Logger' class is
    also being used. Great for providing progress details ( 10%, 20%, ...)
    completion feedback to user during a lengthy process. Content is
    automatically displyed on a single line without text overwrite issues.

    Where:
        <interval> = (optional) Number of Seconds that must pass before
                     a message will be allowed to display.
                     Default is 1

         <verbose> = (optional) Console display behavior.
                     Default is None (minimal) or value of global
                     verbose (see 'getVerboseHandles' function)

    Methods:
        '<object>.display( <message>)' If time, display <message> text to
                                       console.

        '<object>.clear( <message>)' Clear text on console line and display
                                     (optional) message text. <message> will
                                     be logged if 'Logger' class is used, a
                                     NewLine is added to end of text.

        '<object>.willDisplay()' Returns True if calling '<object>.display'
                                 will actually display a message. False if
                                 it's not time to display anything. Use
                                 this to test the display condition before
                                 constructing a complicated message that
                                 involves heavy calculations. Can save un-
                                 necessary processing that will not end up
                                 being displayed to the user anyway.

    Example Use:
        # Read file list, then display Progress while processing files

        Progress = ALFlib.Progress()
        fileList = [ "file.1", "file.2", "file.3", "file.4", ...]
        fileCount = len( fileList)

        for fileNum in range( 0,fileCount,1):
            if Progress.willDisplay():
                percent = float( fileNum) / fileCount
                Progress.display( "{0:.0%} complete!".format( percent))

            DoSomethingWithFileName( fileList[ fileNum])
            ...
            ...

        Progress.clear( "Done!")

"""

    # Initialize Class, default interval to 1 if not provided
    def __init__( self, interval=1, verbose=None):
        self._interval = interval
        self._lastLength = 0
        self._setTimestamp()
        self._handle = utils.getVerboseHandles( verbose)[0]

    # Internal function to set Timestamp to now minus interval, ensuring a display on initial call
    def _setTimestamp( self):
        self._lastTimestamp = datetime.datetime.now() - datetime.timedelta( seconds=self._interval)

    # Display message if it is time
    def display( self, message):
        if self.willDisplay():
            # Only show feedback once a second
            if hasattr( self._handle, "log"):
                logState = self._handle.log
                self._handle.log = False # Turn Off Logging

            # Adjust message (to clear last message if shorter)
            if message:
                thisLength = len(message)
            else:
                thisLength = 0

            if thisLength < self._lastLength:
                message = message + " " * (self._lastLength - thisLength)

            # Display message
            self._lastTimestamp = datetime.datetime.now()
            self._lastLength = thisLength
            self._handle.write( message + "\r")

            if hasattr( self._handle, "log"):
                self._handle.log = logState # Restore Logging

    # Test time interval and see if it is time to display a message
    def willDisplay( self):
        return ((datetime.datetime.now() - self._lastTimestamp).seconds >= self._interval)

    # Clear console line and display optional message
    def clear( self, message=None):
        self._setTimestamp()
        self.display( "")
        if message:
            self._handle.write( message)
            self._handle.write( "\n")
        self._setTimestamp()

##############################################
# Class to manage calls to 's3cmd.py' script #
#                                            #
# Build: v1.0.0, Dec 2012, Paul Dodd - esri  #
##############################################

class S3cmd( object):
    """Class: S3cmd( [<configFile>[, <verbose>]])

    Use this class to manage calls to 's3cmd.py' script. Allowing easy
    download and upload of Amazon S3 content with minimal coding.

    For full details on s3cmd.py, please see: 'http://s3tools.org/s3cmd'

    Requires that the 's3cmd.py' tool has been installed and properly
    configured prior to use. * Note * Be sure to test command line execution
    of 's3cmd.py' as the user that will use this class!

    If 'Errno 10013' is received, check your system's advanced Firewall
    permissions settings to ensure that the Python executable is permitted
    access to the Internet.

    Where:
        <configFile> = (optional) Filename and optional Path to an s3cmd
                       configuration file to include with each call.
                       Default is to allow 's3cmd.py' to use its own
                       default or pre-configured settings.

           <verbose> = (optional) Console display behavior.
                       Default is None (minimal) or value of global
                       verbose (see 'getVerboseHandles' function)

    Built-in Objects:
        S3object = Named Tuple of details for each S3 object(s) returned.
               objectType: Type of Object, 'bucket'; 'directory'; or 'file'
                     name: Text name of object
             lastModified: Datetime object containing last modified date
                      md5: Message Digest hash value of object
                     size: byte size of object
                      URL: Internet path to object
                 mimeType: Text containing mime format of object
               permission: List of 'user:permission' strings

        S3Timeout = Custom exception used to report timeout condition.

        S3InvalidPath = Custom exception used to report an Invalid S3 path.

    Methods:
        '<object>.getInfo( <bucketPath>[, <timeout>[, <verbose>[, <attempts>[, <pause>]]]])'
        '<object>.getList( [<bucketPath>[, <timeout>[, <verbose>]]])'
        '<object>.putFile( <source>, <bucketPath>[, <returnInfo>[, <callOptions>[, <makePublic>[, <reducedRedundancy>[, <recursive>[, <timeout>[, <verbose>]]]]]])'
        '<object>.getFile( <bucketPath>[, <destination>[, <callOptions>[, <recursive>[, <timeout>[, <verbose>, <pollHook>]]]]])'

    Example Use:
        # Get list of items stored in S3 Bucket

        import ALFlib

        s3 = ALFlib.S3cmd( configFile="c:\\Project\\s3config.ini")

        for item in s3.getList( "s3://MyBucket"):
            print( "\\n    S3 object: ({0}) '{1}'".format( item.objectType,
                                                           item.name))
            print( "Last Modified: {0}".format( item.lastModified))
            print( "         Size: {0}".format( item.size))
            print( "     MD5 hash: {0}".format( item.md5))

"""

    # Custom Exceptions

    class S3InvalidPath( Exception):
        pass

    # Local Functions
    def __init__( self, configFile=None, verbose=None):
        # Setup List / Info class object
        self.S3object = collections.namedtuple( "S3object", [  "objectType", "name", "lastModified", "md5", "size", "URL", "mimeType", "permission"])

        # Setup initial command line start process options
        if os.name == "nt":
            initialPath = os.path.join( os.path.split( sys.executable)[0], "Scripts\\")

            # Scripts folder available?
            if os.access( initialPath, os.F_OK):
                # Look for s3cmd.py script
                if os.access( initialPath + "s3cmd.py", os.F_OK):
                    self.CMD = [
                        sys.executable,
                        initialPath + "s3cmd.py"
                    ]
                # Look for s3cmd script
                elif os.access( initialPath + "s3cmd", os.F_OK):
                    self.CMD = [
                        sys.executable,
                        initialPath + "s3cmd"
                    ]
                else:
                    # Fallback to letting os find and launch script its self
                    self.CMD = [ "s3cmd.py"]
            else:
                # Fallback to letting os find and launch script its self
                self.CMD = [ "s3cmd.py"]
        else:
            self.CMD = [ "s3cmd"]

        if configFile:
            self.CMD += ["-c", configFile]

        verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

        try:
            outcome, response = utils.callCommandLine( self.CMD + ["--version"], description="Checking Availability", verbose=verbose)

            if outcome == 0:
                verboseDetail.write( " * Success!\n")
            else:
                raise Exception( "[Errno {0}], {1}".format( outcome, response))

        except Exception as e:
            raise Exception( "{0}\n * Unable to locate 's3cmd' tool. Please verify installation!".format( e))

    # Check bucket path and return result
    def checkPath( self, bucketPath):
        """Internal method, not intended for general use."""
        if bucketPath:
            if isinstance( bucketPath, basestring):
                bucket = bucketPath.replace( "\\", "/")
                if bucket.lower().startswith( "s3://"):
                    return bucket

            raise self.S3InvalidPath( "Invalid S3 path specified: '{0}'".format( bucketPath))
        else:
            return ""

    # Return informational detail of s3 object
    def getInfo( self, bucketPath, timeout=5, verbose=None, attempts=1, pause=10):
        """Method: getInfo( <bucketPath>[, <timeout>[, <verbose>[, <attempts>[, <pause>]]]])

    Returns S3object for specified <bucketPath> item.

    <bucketPath> = S3 bucket, directory, or file path.
                   Like 's3://MyBucket/dir/item.name'

       <timeout> = (optional) Time in seconds the process should wait
                   before item is considered not to exist.
                   Default is 5 seconds.

       <verbose> = (optional) Console display behavior.
                   Default is None (minimal) or value of global
                   verbose (see 'getVerboseHandles' function)

      <attempts> = (optional) Number of attempts to collect item info from S3
                   Default is 1

         <pause> = (optional) Number of seconds to pause between <attempts>
                   Default = 10
"""
        # Setup Verbose Object
        verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

        # Check Timeout
        if not timeout:
            timeout = 300	# Reset to 5 minutes to force a timeout, not allowing
                                    # command to lock process if item does not exist!

        dateMask = "%d %b %Y %H:%M:%S"

        callOptions = self.CMD + [
            "info",
            self.checkPath( bucketPath)
        ]

        type="unknown"
        name = ""
        lastModified = None
        md5 = ""
        size = 0
        URL = ""
        mimeType = ""
        permission = []

        try:
            response = utils.retryIt( utils.callCommandLine, [callOptions], kwargs={ "timeout": timeout, "verbose": verbose, "description": "Getting object Info"}, attempts=attempts, pause=pause)[1]

            for buffer in response:
                if buffer.upper().find( "ERROR:") >= 0:
                    raise Exception( "Detected 'Error' in s3 command response, please investigate!")

                col = buffer.split()
                cols = len(col)

                if cols > 1:
                    if col[0].startswith( "s3://"):
                        name = " ".join( col[0:-1])    # Reassemble list less right-most element
                        if col[-1] == "(bucket):":    # Check right-most element
                            type = "bucket"
                            break
                        elif name.endswith( "/"):
                            type = "directory"
                        else:
                            type = "file"
                    elif col[0] == "File" and col[1] == "size:":
                        size = int(col[2])
                    elif col[0] == "Last" and col[1] == "mod:":
                        lastModified = datetime.datetime.strptime( "{0} {1} {2} {3}".format( col[3], col[4], col[5], col[6]), dateMask)
                    elif col[0] == "MD5" and col[1] == "sum:":
                        md5 = col[2]
                    elif col[0] == "URL:":
                        URL = col[1]
                    elif col[0] == "MIME" and col[1] == "type:":
                        mimeType = col[2]
                    elif col[0] == "ACL:":
                        permission.append( col[1] + col[2])

            verboseDetail.write( " * Success!\n")

            return self.S3object( type, name, lastModified, md5, size, URL, mimeType, permission)

        except utils.TimeoutError:
            verboseCasual.write( " * Info request 'Timed Out', assuming S3 object does not exist!\n")
            return None

    # Return list detail for s3 object(s)
    def getList( self, bucketPath=None, timeout=5, verbose=None):
        """Method: getList( [<bucketPath>[, <timeout>[, <verbose>]]])

    Returns list containing one or more S3objects depending on <bucketPath>.

    <bucketPath> = (optional) S3 bucket, directory, or file path.
                   Like 's3://MyBucket'. To received a directory's
                   contents, be sure to include a trailing '/'.
                   Default is None, returns objects in root level
                   directory (listing all objects).

       <timeout> = (optional) Time in seconds the process should wait
                   before giving up.
                   Default is 5 seconds.

       <verbose> = (optional) Console display behavior.
                   Default is None (minimal) or value of global
                   verbose (see 'getVerboseHandles' function)
"""
        # Setup Verbose Object
        verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

        items = []
        dateMask = "%Y-%m-%d %H:%M"

        #callOptions = [
        callOptions = self.CMD + [
            "--list-md5"
        ]

        if bucketPath:
            callOptions.append( "ls")
            callOptions.append( self.checkPath( bucketPath))
        else:
            callOptions.append( "la")

        for buffer in utils.callCommandLine( callOptions, timeout=timeout, verbose=verbose, description="Getting object List")[1]:
            if buffer.upper().find( "ERROR:") >= 0:
                raise Exception( "Detected 'Error' in s3 command response, please investigate!")

            col = buffer.split()
            cols = len(col)

            if cols > 1:
                if col[0] == "DIR":
                    items.append( self.S3object( "directory", " ".join( col[1:]), None, "", 0, "", "", []))
                elif cols > 2 and col[0][4:5] == "-" and col[0][7:8] == "-" and col[1][2:3] == ":":
                    if col[2].startswith( "s3://"):
                        items.append( self.S3object( "bucket", " ".join( col[2:]), datetime.datetime.strptime( "{0} {1}".format( col[0], col[1]), dateMask), "", 0, "", "", []))
                    elif col[4].endswith( "/"):
                        items.append( self.S3object( "directory", " ".join( col[4:]), datetime.datetime.strptime( "{0} {1}".format( col[0], col[1]), dateMask), col[3], 0, "", "", []))
                    else:
                        items.append( self.S3object( "file", " ".join( col[4:]), datetime.datetime.strptime( "{0} {1}".format( col[0], col[1]), dateMask), col[3], int(col[2]), "", "", []))

        if len( items) == 1:
            verboseDetail.write( " * Success, list contains 1 item!\n")
        else:
            verboseDetail.write( " * Success, list contains {0} items!\n".format( len( items)))

        return items

    # Upload file to S3 bucket
    def putFile( self, source, bucketPath, returnInfo=False, callOptions=[], makePublic=False, reducedRedundancy=False, recursive=False, timeout=None, verbose=None):
        """Method: putFile( <source>, <bucketPath>[, <returnInfo>[, <callOptions>[, <makePublic>[, <reducedRedundancy>[, <recursive>[, <timeout>[, <verbose>]]]]]])

    Uploads content specified by <source> to location <bucketPath>, returning a
    list of S3objects containing details for each item uploaded.

               <source> = File or Directory (if recursive) path to content that
                          will be uploaded.

           <bucketPath> = S3 bucket, directory, or file path.
                          Like 's3://MyBucket/MyPath/'.

           <returnInfo> = (optional) True or False. Whether to query each
                          uploaded item for details, supplementing S3object
                          info returned.
                          Default is False.

          <callOptions> = (optional) List of additional 's3cmd' command line
                          options to include with call.
                          See 's3cmd' help for full list.

           <makePublic> = (optional) True or False. Whether to allow public
                          access to item(s) being uploaded.
                          Default is False.

    <reducedRedundancy> = (optional) Enable Reduced Redundancy storage option.
                          Default is False (fully redundant)

            <recursive> = (optional) Whether to recursively upload contents of
                          specified directory.
                          Default is False

              <timeout> = (optional) Time in seconds the process should wait
                          before giving up.
                          Default is None (no timeout)

              <verbose> = (optional) Console display behavior.
                          Default is None (minimal) or value of global
                          verbose (see 'getVerboseHandles' function)
"""
        # Setup Verbose Object
        verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

        options = self.CMD[0:]
        if callOptions:
            if isinstance( callOptions, list):
                options += callOptions
            else:
                options.append( callOptions)
        options.append( "put")

        if source:
            if isinstance( source, list):
                options += source
            else:
                options.append( source)

        if bucketPath:
            options.append( self.checkPath( bucketPath))

        if makePublic:
            options.append( "--acl-public")

        if reducedRedundancy:
            options.append( "--reduced-redundancy")

        if recursive:
            options.append( "--recursive")

        items = []

        for buffer in utils.callCommandLine( options, timeout=timeout, verbose=verbose, description="Uploading file object(s)")[1]:
            if buffer.upper().find( "ERROR:") >= 0:
                raise Exception( "Detected 'Error' in s3 command response, please investigate!")

            col = buffer.split("'")
            cols = len(col)

            if cols > 4:
                if col[3].startswith( "s3://"):
                    if returnInfo:
                        if timeout:
                            items.append( self.getInfo( col[3], timeout=timeout, verbose=verbose))
                        else:
                            items.append( self.getInfo( col[3], verbose=verbose))
                    else:
                        items.append( self.S3object( "file", col[3], None, "", int(col[4][2:].split()[0]), "", "", []))

        if len( items) == 1:
            verboseDetail.write( " * Successfully uploaded 1 file!\n")
        else:
            verboseDetail.write( " * Successfully uploaded {0} files!\n".format( len( items)))

        return items

    # Download file from S3 bucket
    def getFile( self, bucketPath, destination=None, callOptions=[], recursive=False, timeout=None, verbose=None, timerHook=None):
        """Method: getFile( <bucketPath>[, <destination>[, <callOptions>[, <recursive>[, <timeout>[, <verbose>, <pollHook>]]]]])

    Download content specified by <bucketPath>.

     <bucketPath> = S3 path to bucket, directory, and file to download.
                    Like 's3://MyBucket/MyPath/MyFile.txt'.

    <destination> = (optional) Path or Filename where content will be
                    downloaded.
                    Default is current location and name of content
                    being downloaded.

    <callOptions> = (optional) List of additional 's3cmd' command line
                    options to include with call.
                    See 's3cmd' help for full list.

      <recursive> = (optional) Whether to recursively download content
                    from specified <bucketPath>.
                    Default is False

        <timeout> = (optional) Time in seconds the process should wait
                    before giving up.
                    Default is None (no timeout)

        <verbose> = (optional) Console display behavior.
                    Default is None (minimal) or value of global
                    verbose (see 'getVerboseHandles' function)

      <timerHook> = (optional) Function name to call during the process
                    'timeout' monitor loop (see 'callCommandLine'
                    function for full details).
                    Default is None
"""
        # Setup Verbose Object
        verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

        options = self.CMD[0:]
        if callOptions:
            if isinstance( callOptions, list):
                options += callOptions
            else:
                options.append( callOptions)
        options.append( "get")

        if bucketPath:
            options.append( self.checkPath( bucketPath))

        if destination:
            options.append( destination)

        if recursive:
            options.append( "--recursive")

        items = []

        for buffer in utils.callCommandLine( options, timeout=timeout, verbose=verbose, description="Downloading file object(s)", timerHook=timerHook)[1]:
            if buffer.upper().find( "ERROR:") >= 0:
                raise Exception( "Detected 'Error' in s3 command response, please investigate!")

            col = buffer.split("'")
            cols = len(col)

            if cols > 2:
                col[0] = col[0].split()
                if len(col[0]) > 1 and col[0][0] == "File" and col[0][1].startswith( "s3://"):
                    items.append( self.S3object( "file", os.path.realpath( col[1]), None, "", int(col[2][2:].split()[0]), "", "", []))

        if len( items) == 1:
            verboseDetail.write( " * Successfully downloaded 1 file!\n")
        else:
            verboseDetail.write( " * Successfully downloaded {0} files!\n".format( len( items)))

        return items

class StopWatch( object):
    """Class: StopWatch()

    Use this class to time events or processes. When started, it will record and
    return the current datetime, and clear all counters. When stopped, it will
    record the final ending datetime, lap time, and then return the elapsed
    timedelta.

    Access the 'elapsedTime' and 'lapTime' properties at any time to receive the
    current timedelta for each. Use the 'lap' method to record and then return
    the current lap time timedelta, resetting the counter for the next lap. A
    list of the recorded lap times can be retrieved by accessing the 'lapTimes'
    property.

    Methods:

        '<object>.start()' Set or reset the start time, clearing all counters.
                           Returns the starting datetime value.

        '<object>.stop()' Set the ending time, record the final lap, and stop
                          the clock.
                          Returns the elapsed time as a timedelta.

        '<object>.lap()' Record the current lap time, resetting counter.
                         Returns the current lap time as a timedelta.

        '<object>.lapAvg()' Average the elapsed time by the number of laps.
                            Returns a timedelta.

    Properties:

        '<object>.startTime' Return the start datetime or None if not started.

        '<object>.stopTime' Return the ending datetime or None if not stopped.

        '<object>.elapsedTime' Return the elapsed time as a timedelta.

        '<object>.lapTime' Return the current lap time as a timedelta.

        '<object>.lapTimes' Return a copy of all lap times as a list.

    Example Use:

        from ALFlib import StopWatch

        sw = StopWatch()

        print( "Process started: {0}".format( sw.start()))

        #...do some work...
        print( sw.lap())

        #...do some more work...
        print( sw.lap())

        #...run final logic...
        sw.stop()
        print( "Process finished: {0} (Elapsed Time: {1})".format( sw.stopTime, sw.elapsedTime))
        print( "Average Lap Time: {0}".format( sw.lapAvg()))
"""

    def __init__( self):
        self._startTime = None
        self._endTime = None
        self._lapStart = None
        self._laps = []

    def start( self):
        """Set/Reset the starting time, marking and returning the begin datetime."""
        # Reset
        self.__init__()
        now = datetime.datetime.now()
        self._startTime = now
        self._lapStart = now

        # Return start datetime
        return now

    @property
    def startTime( self):
        """Get the start datetime or None if it hasn't started."""
        return self._startTime

    def stop( self):
        """Set the ending time, stopping the clock and returning the total elapsed time as a timedelta."""
        if self._startTime:
            if not self._endTime:
                self._endTime = datetime.datetime.now()
                self._laps.append( self._endTime - self._lapStart)
            return self._endTime - self._startTime
        else:
            return datetime.timedelta()

    @property
    def stopTime( self):
        """Get the ending datetime or None if it hasn't ended."""
        return self._endTime

    @property
    def elapsedTime( self):
        """Get the current elapsed timedelta."""
        if self._startTime:
            if self._endTime:
                return self._endTime - self._startTime
            else:
                return datetime.datetime.now() - self._startTime
        else:
            return datetime.timedelta()

    def lap( self):
        """Record and return the elapsed timedelta since the last lap."""
        if self._startTime:
            if not self._endTime:
                now = datetime.datetime.now()
                self._laps.append( now - self._lapStart)
                self._lapStart = now
            return self._laps[-1]
        else:
            return datetime.timedelta()

    def lapAvg( self):
        """Get the average lap time timedelta from elapsed time / number of laps."""
        if self._startTime:
            if self._endTime:
                return (self._endTime - self._startTime) / len( self._laps)
            else:
                return (datetime.datetime.now() - self._startTime) / (len( self._laps) + 1)
        else:
            return datetime.timedelta()

    @property
    def lapTime( self):
        """Get the current lap timedelta."""
        if self._startTime:
            if self._endTime:
                return self._laps[-1]
            else:
                return datetime.datetime.now() - self._lapStart
        else:
            return datetime.timedelta()

    @property
    def lapTimes( self):
        """Get a copy of the recorded lap times as a list of timedeltas."""
        if self._startTime:
            if not self._endTime:
                return self._laps[:] + [datetime.datetime.now() - self._lapStart]
        return self._laps[:]

#################################################
# Return next 'spinner' symbol from symbol list #
#                                               #
# Build: v1.0.0, Aug 2013, Paul Dodd - esri     #
#################################################

class Spinner( object):
    """Class: Spinner( [<symbols>])

    Return the next 'spinner' symbol in the 'symbols' list. Great for creating
    feedback using a spinning star symbol.

    Where:
        <symbols> = (optional) Is the String of symbols to spin through. Use
                    the next and prior properties to step through characters.
                    Default is a character string containing: '-\\|/'

    Properties:

        '<objext>.symbols' (string) Get or Set current set of symbols.

        '<objext>.next' (string) Returns the next character to the right.

        '<objext>.prior' (string) Returns the prior character to the left.

    Example Usage:

        import ALFlib, time, sys

        spin = ALFlib.Spinner()

        for loop in range(10):
            # Write symbol to console, but do not advance to next line!
            sys.stdout.write( "\\r" + spin.next)

            # Sleep for 1/4 second
            time.sleep( 0.25)
"""
    def __init__( self, symbols="-\\|/"):
        if not (symbols and isinstance( symbols, basestring)):
            symbols = "-\\|/"

        self._index = 0
        self._symbolSet= symbols
        self._symbolChain = []

        for index in range( len( symbols)):
            self._symbolChain.append( [index + 1, index - 1])
        self._symbolChain[-1][0] = 0
        self._symbolChain[0][1] = len( symbols) - 1

    @property
    def symbols(self):
        """Get current symbol set"""
        return self._symbolSet

    @symbols.setter
    def symbols( self, symbols):
        """Set current symbol set"""
        self.__init__( symbols)

    @property
    def next( self):
        """Return next character, going left to right"""
        self._index = self._symbolChain[ self._index][ 0]
        return self._symbolSet[ self._index]

    @property
    def prior( self):
        """Return prior symbol character, going right-to-left"""
        self._index = self._symbolChain[ self._index][ 1]
        return self._symbolSet[ self._index]

###############################################
# Augment os.environ environment dictionary   #
#                                             #
# Uses local environment file to add, delete, #
# or override system environment variables.   #
###############################################

def augmentEnviron( envFile="ALFlib_env.py", verbose=None):
    """Function: augmentEnviron( [<envFile>[, <verbose>]])

    Alters 'os.environ' Environment Variable Dictionary based on environment file.

    Where:
        <envFile> = (optional) Filename and optional Path to Python file that
                    contains the variable entries to apply.
                    Default file is 'ALFlib_env.py'

        <verbose> = (optional) Console display behavior.
                    Default is None (minimal) or value of global
                    verbose (see 'getVerboseHandles' function)

    File Path search priority:
        1 = Literal path of <envFile>, if path included
        2 = Current directory, if path not included in <envFile>
        3 = Path location of 'ALFlib.py'
        4 = Hierarchal System Path Environment Variable, deepest first!

    Within file:
        Add new or Update existing variables by using '<variable> = <value>'
        Delete existing variables by using '<variable> = None'

        * Note * Routine will only apply variable types that match:
                'bool, int, long, float, str, unicode, datetime.date,
                datetime.date, or datetime.datetime'.
                Environment Varible values are applied as Unicode strings!

    Changes will immediately be available to the 'os.environ' Dictionary.
    Scripts that use the 'Logger' class will automatically receive updates
    during next Logger initialization cycle.
"""
    # Get verbose handles
    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    def loadFile( envFile):
        # Load file contents and return locals Dictionary (less envFile)
        execfile( envFile)
        del envFile
        return locals()

    files = []
    # Find file(s)
    if os.access( envFile, os.F_OK) and ( "/" in envFile or  "\\" in envFile):
        # Handle specification of a literal or relative path to file
        files.append( os.path.realpath( envFile))
    else:
        envFile = os.path.split( envFile)[1]    # Extract just file name and extension
        root = os.path.split( os.path.realpath(__file__))[0]

        # Add ALFlib home to Path if not already available
        if root and root not in sys.path:
            sys.path.insert( 0, root)

        # Search path for file
        for path in sys.path + os.environ.get( "PATH", "").split( ";"):
            sFile = os.path.realpath( os.path.join( path, envFile))
            if os.access( sFile, os.F_OK) and sFile not in files:
                files.insert( 0, sFile)

    for envFile in files:
        #envFile = os.path.realpath( envFile)
        localVars = {}

        # Import file contents
        try:
            localVars = loadFile( envFile)
            verboseCasual.write( "\nAugmenting Environment w/File: '{0}'\n".format( envFile))

        except Exception as e:
            verboseCasual.write( "\n * 'ALFlib.augmentEnviron' Failed to load Environment File: '{0}', Error: '{1}'\n".format( envFile, e))

        # Check for variables and apply to os.environ
        for key, value in localVars.items():
            if type( value) in [ bool, int, long, float, str, unicode, datetime.date, datetime.time, datetime.datetime]:
                # Apply addition or change
                verboseDetail.write( " - Setting: '{0}'\n".format( key))
                try:
                    os.environ[ key] = str( value)
                except Exception as e:
                    verboseCasual.write( "\n * 'ALFlib.augmentEnviron' Failed to set '{0} = {1}', Error: '{2}'\n".format( key, value, e))

            elif key in os.environ and isinstance( value, type( None)):
                # If value is None and variable exists, delete it!
                verboseDetail.write( " -Removing: '{0}'\n".format( key))
                try:
                    del os.environ[ key]
                except Exception as e:
                    verboseCasual.write( "\n * 'ALFlib.augmentEnviron' Failed to remove '{0}', Error: '{1}'\n".format( key, e))

#####################################################
# Get Environment Variable as Specified Object Type #
#                                                   #
# Build: v1.0.0, Dec 2015, Paul Dodd - esri         #
#####################################################

def getEnviron( varName, objType=unicode, default=None, verbose=None):
    """Function: getEnviron( <varName>[, <objType>[, <verbose>]])

    Get Environment Variable value as a specified object type.

    Returns:
        Value of Environment Variable <varName> as object type <varType>
        Or <default> if not available or when there are issues. An error
        notation will be sent to standard error out for diagnostics when
        <verbose> available.

    Where:
        <varName> = Environment Variable to access

        <objType> = (optional) Valid Object type to generate using
                    environment variable string value accessed.
                    Type 'bool' returns False if environment variable value
                    is equal to a case-insensitive check to any of:
                        'false', 'off', 'no', '0', '0.0', or '-0.0'
                    Type 'int' and 'long' will return integer of value.
                    Type 'list' will return list from value split on ';'
                    Default return type is a Unicode string

        <default> = (optional) Default value to return if environment
                    variable is not found or if issues are encountered.
                    Default is None

        <verbose> = (optional) Console display behavior.
                    Default is None (minimal) or value of global
                    verbose (see 'getVerboseHandles' function)
"""
    # Get verbose handles
    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    value = os.environ.get( varName)

    if value is None:
        return default

    # Clean whitespaces
    value = value.strip()

    try:
        if objType is bool:
            # Special handling required
            return not (not value or value.lower() in ["false", "no", "off", "0", "0.0", "-0.0"])

        elif objType in [int, long]:
            # Special handling required
            return objType( value.split( ".")[0])

        elif objType is list:
            return value.split( ";")

        return objType( value)

    except Exception as e:
        try:
            objName = objType.__name__
        except:
            try:
                objName = type( objType).__name__
            except:
                try:
                    objName = repr( objType)
                except:
                    objName = "Unknown"

        verboseDetail.write( " * ALFlib.getEnviron * Unable to generate object type: '{2}' for Environment Variable: '{0}={1}', error: {3}\n".format( varName, value, objName, e))
        return default

###########################################################
# Return progress bar content, filled to given percentage #
#                                                         #
# Build: v1.0.0, Paul Dodd - esri                         #
###########################################################

def progressBar( percent, size=20, left='[', right=']', marker='>', trailer='=', filler=' ', show=True):
    """Function: progressBar( <percent>[, <size>[, <left>[, <right>[, <marker>[, <trailer>[, <filler>[, <show>]]]]]]])

    Return progress bar text string filled to given percentage with 'trailer'
    characters to the left and an indicator of 'marker', padded to the right with
    'filler' characters, surrounded by 'left' and 'right' end characters. Great
    for displaying a progress bar showing the level of completion. By default,
    the percentage of completion is displayed in the center.

    Where:
        <percent> = Whole number (0 to 100) or float percentage (0.0 to 1.0)
                    that reflects the percentage of completion.
           <size> = (optional) Number of display characters to use, not
                    including 'left' and 'right' encapsulation characters.
                    Default = 20
           <left> = (optional) Character to use for left-side encapsulation.
                    Default = '['
          <right> = (optional) Character to use for right-side encapsulation.
                    Default = ']'
         <marker> = (optional) Character indicating level of completion.
                    Default = '>'
        <trailer> = (optional) Character trailing <marker>.
                    Default = '='
         <filler> = (optional) Character to use as filler in front of <marker>.
                    Default = ' '
           <show> = (optional) Display completion percentage centered in text.
                    Default = True

    Example Usage:

        import ALFlib, time, sys

        for loop in range(100):
            # Write progress bar to console, but do not advance to next line!
            #sys.stdout.write( "\\r" + ALFlib.progressBar( loop, marker='+', size=5))
            # or
            sys.stdout.write( "\\r" + ALFlib.progressBar( float(loop) / 100))

            # Sleep for 1/4 second
            time.sleep( 0.25)

    Example output: '[====>    25%        ]'
"""
    if isinstance( percent, long) or isinstance( percent, int) or isinstance( percent, float):
        if percent <= 0.0:
            percent = 0.0
        elif percent <= 1.0 and isinstance( percent, float):
            percent = float( percent)
        elif 1.0 <= percent <= 100.0:
            percent = float( percent) / 100
        else:
            percent = 1.0
    else:
        percent = 1.0

    if not size: size = 20
    if not (marker and isinstance( marker, basestring)): marker = ">"
    if not (trailer and isinstance( trailer, basestring)): trailer = "="
    if not (filler and isinstance( filler, basestring)): filler = " "

    trailerSize = int( size * percent)
    fillerSize = size - trailerSize - 1

    if trailerSize == size:
        marker = ""
    else:
        marker = marker[0]

    output = left + (trailer[0] * trailerSize) + marker + (filler[0] * fillerSize) + right

    if show and size >= 4:
        percentage = "{0:.0%}".format( percent)
        lp = len( percentage)
        offset = (len( output) / 2) - int( lp / 2)
        if offset > 0:
            output = output[0:offset] + percentage + output[offset + lp:]

    return output

######################################################
# Convert Degrees.Minutes.Seconds to Decimal Degrees #
#                                                    #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri          #
#     - Restructured code to better adhere to Python #
#       standards and best practices.                #
# Build: v1.0.0, Feb 2012, Paul Dodd - esri          #
######################################################

def dms2dd( degrees=None, minutes=None, seconds=None, bearing=None):
    # Convert Degrees, Minutes, and Seconds to Decimal Degrees

    """Function: dms2dd( [<degrees>[, <minutes>[, <seconds>[, <bearing>]]]])

    Convert Geographical Coordinates from Degrees.Minutes.Seconds
    to Decimal Degrees, returning a float value.

    Where:
        <degrees> = (optional) Angular Degree from -180 to 180
                    Default is None
        <minutes> = (optional) Angular Minute from 0 to 59
                    Default is None
        <seconds> = (optional) Angular Second from 0 to 59
                    Default is None
        <bearing> = (optional) Directional bearing, can be:
                    (default) None = Preserve +- polarity of <degrees>
                    'N','n','E','e' = Return Positive value
                    'S','s','W','w' = Return Negative value
"""

    dDegrees = 0

    try:
        if degrees:
            degrees = float( degrees)
        else:
            degrees = 0

        if minutes:
            minutes = abs( float( minutes)) / 60
        else:
            minutes = 0

        if seconds:
            seconds = abs( float( seconds)) / 3600
        else:
            seconds = 0

        if degrees >= 0:
            dDegrees = degrees + minutes + seconds
        else:
            dDegrees = degrees - minutes - seconds

        if bearing:
            if bearing.upper() == "W" or bearing.upper() == "S":
                dDegrees = abs( dDegrees) * -1
            elif bearing.upper() == "E" or bearing.upper() == "N":
                dDegrees = abs( dDegrees)

    except:
        pass

    return dDegrees

######################################################
# Convert Celsius Temperature to Fahrenheit          #
#                                                    #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri          #
#     - Restructured code to better adhere to Python #
#       standards and best practices.                #
# Build: v1.0.0, Mar 2012, Paul Dodd - esri          #
######################################################

def c2f( tempCelsius):
    # Convert Celsius to Fahrenheit

    """Function: c2f( <tempCelsius>)

    Convert Celsuis Temperature to Fahrenheit, returning a float value.

    Where:
        <tempCelsius> = (required) A float or integer temperature in
                        Celsius units.
"""

    return 9.0 / 5.0 * tempCelsius + 32.0

######################################################
# Convert Fahrenheit Temperature to Celsius          #
#                                                    #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri          #
#     - Restructured code to better adhere to Python #
#       standards and best practices.                #
# Build: v1.0.0, Mar 2012, Paul Dodd - esri          #
######################################################

def f2c( tempFahrenheit):
    # Convert Fahrenheit to Celsius

    """Function: f2c( <tempFahrenheit>)

    Convert Fahrenheit Temperature to Celsuis, returning a float value.

    Where:
        <tempFahrenheit> = (required) The float or integer temperature
                           in Fahrenheit units.
"""

    return 5.0 / 9.0 * (tempFahrenheit - 32.0)

###############################################
# Weather - Compute Heat Index from Celsius   #
# Temperature and Percent Humidity            #
#                                             #
# Build: v1.0.2, Feb 2014, Paul Dodd - esri   #
#     - corrected 'c5' value                  #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri   #
#     - Restructured code to better adhere to #
#       Python standards and best practices.  #
# Build: v1.0.0, Mar 2012, Paul Dodd - esri   #
###############################################

def heatIndex( tempCelsius, percentHumidity):
    # Compute Heat Index from Temperature and Relative Humidity Percentage
    # Source: http://www.hpc.ncep.noaa.gov/html/heatindex_equation.shtml
    # Source: https://en.wikipedia.org/wiki/Heat_index

    """Function: heatIndex( <tempCelsius>, <percentHumidity>)

    Compute Heat Index from Dry-bulb Temperature and Percent Humidity,
    returning a float value in Celsius.

    Where:
            <tempCelsius> = (required) The float or integer temperature
                            in Celsius.
        <percentHumidity> = (required) The float or integer Humidity as
                            a percentage. * Note * a humidity of 66.5%
                            is supplied as '66.5' not '.665'
"""

    T = c2f( tempCelsius)	# convert to Fahrenheit
    R = percentHumidity
    HI = 0.0

    if T >= 80.0:
        # Primary Formula Constants, more accurate (+-1.3F) with limited range
        c1 = -42.379
        c2 = 2.04901523
        c3 = 10.14333127
        c4 = -0.22475541
        c5 = -0.00683783
        c6 = -0.05481717
        c7 = 0.00122874
        c8 = 0.00085282
        c9 = -0.00000199

        HI = c1 + c2*T + c3*R + c4*T*R + c5*T*T + c6*R*R + c7*T*T*R + c8*T*R*R + c9*T*T*R*R

        if R < 13.0 and T > 80.0 and T < 112.0:
            # Adjust according to 'http://www.hpc.ncep.noaa.gov/html/heatindex_equation.shtml'
            HI -= ((13.0 - R) / 4) * math.sqrt((17.0 - abs(T-95.0)) / 17.0)

        if R > 85.0 and T > 80.0 and T < 87.0:
            # Adjust according to 'http://www.hpc.ncep.noaa.gov/html/heatindex_equation.shtml'
            HI += ((R - 85.0) / 10.0) * ((87.0 - T) / 5.0)

    if HI < 80.0 and R <= 80.0 and T >= 70.0 and T <= 115.0:
        # Alternate Formula with greater range, used when method 1 produces a Heat Index < 80
        # Or when temp is less than 80
        c1 = 16.923
        c2 = 0.185212
        c3 = 5.37941
        c4 = -0.100254
        c5 = 0.00941695
        c6 = 0.00728898
        c7 = 0.000345372
        c8 = -0.000814971
        c9 = 0.0000102102
        c10 = -0.000038646
        c11 = 0.0000291583
        c12 = 0.00000142721
        c13 = 0.000000197483
        c14 = -0.0000000218429
        c15 = 0.000000000843296
        c16 = -0.0000000000481975

        HI = c1 + c2*T + c3*R + c4*T*R + c5*T*T + c6*R*R + c7*T*T*R + c8*T*R*R + c9*T*T*R*R + c10*T*T*T + c11*R*R*R + c12*T*T*T*R + c13*T*R*R*R + c14*T*T*T*R*R + c15*T*T*R*R*R + c16*T*T*T*R*R*R
    elif not HI:
        # Outside defined limits
        return

    # Return value in Celsius
    return f2c( HI)

######################################################
# Weather - Compute Relative Humidity from Celsius   #
# Temperature and DewPoint                           #
#                                                    #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri          #
#     - Restructured code to better adhere to Python #
#       standards and best practices.                #
# Build: v1.0.0, Mar 2012, Paul Dodd - esri          #
######################################################

def relativeHumidity( tempCelsius, dewPointCelsius):
    # Compute Relative Humidity from Temperature and Dew Point
    # Source: http://www.gorhamschaffler.com/humidity_formulas.htm

    """Function: relativeHumidity( <tempCelsius>, <dewPointCelsius>)

    Compute Relative Humidity from Celsius Temperature and DewPoint,
    returning a percentage value as float.

    Where:
            <tempCelsius> = (required) The float or integer Dry-bulb
                            temperature in Celsius units.
        <dewPointCelsius> = (required) The float or integer DewPoint
                            temperature in Celsius units.
"""

    # Compute Saturation Vapor Pressure in millibars
    Es = 6.11 * pow( 10, 7.5 * float( tempCelsius) / (237.7 + tempCelsius))

    # Compute Actual Vapor Pressure in millibars
    E = 6.11 * pow( 10, 7.5 * float( dewPointCelsius) / (237.7 + dewPointCelsius))

    return (E / Es) * 100

###############################################
# Weather - Compute Wind Chill Factor from    #
# Celsius Temperature and Wind Speed in Km/h  #
#                                             #
# Build: v1.0.1, Apr 2012, Paul Dodd - esri   #
#     - Restructured code to better adhere to #
#       Python standards and best practices.  #
# Build: v1.0.0, Mar 2012, Paul Dodd - esri   #
###############################################

def windChill( tempCelsius, windSpeedKmh):
    # Compute Wind Chill from Temperature and Wind Speed
    # Using North American Wind Chill Index (Nov 2001)
    # Source: https://en.wikipedia.org/wiki/Wind_chill

    """Function: windChill( <tempCelsius>, <windSpeedKmh>)

    Compute Wind Chill Factor from Temperature and Wind Speed,
    returning a float Temperature value in Celsius.

    Where:
         <tempCelsius> = (required) The float or integer temperature
                         in Celsius.
        <windSpeedKmh> = (required) The float or integer Wind Speed
                         in Km/h.
"""

    Ta = tempCelsius
    V = windSpeedKmh

    if Ta > 10:
        # Outside defined limits
        return

    return 13.12 + 0.6215*Ta - 11.37*pow(V, 0.16) + 0.3965*Ta*pow(V, 0.16)

###################################################
# Download web or network file to local system    #
# using native urllib2 routine.                   #
#                                                 #
# Build: v1.7.1, December 2016, Paul Dodd - esri  #
#     - Pathced cache control dictionary issue.   #
#     - Updated to handle ftplib error 550        #
#     - Updated for SSL support                   #
#     - Updated for direct <data> inclusion       #
# Build: v1.7.0, April 2015, Paul Dodd - esri     #
#     - Altered to leverage 'iterPath' function.  #
# Build: v1.6.0, October 2014, Paul Dodd - esri   #
#     - Added logic for restartable transfers,    #
#       indicated by display status.              #
#     - Updated FTP logic to support Buffers.     #
#     - Increased default Buffer size to 8MB      #
#     - Added display detail showing overall      #
#       progress details, elapsed time and speed. #
#     - Added option for setting request headers. #
#     - Added verbose report of request headers.  #
# Build: v1.5.0, May 2014, Paul Dodd - esri       #
#     - Enhanced 'timeStamping' to support stale  #
#       data source detection when set to a       #
#       'datetime.timedelta' value. An Exception  #
#       will be thrown when source age is older   #
#       than now minus this value.                #
#     - Patched Final section of main try block   #
#       to bubble up exception on 'error'.        #
# Build: v1.4.0, March 2014, Paul Dodd - esri     #
#     - Added remote file download and compare    #
#       when 'timeStamping' is None and remote    #
#       file details match local file.            #
# Build: v1.3.1, May 2013, Paul Dodd - esri       #
#     - Patched to remove residual text displayed #
#       during progress.                          #
#     - Refined download to report when access to #
#       remote file's "last-modified" time is not #
#       available, relying on file size check.    #
#     - Added 'If-Modified-Since' html header to  #
#       http-based download requests.             #
#     - Added '<', '~', '>' to local and remote   #
#       file size reporting.                      #
# Build: v1.3.0, January 2013, Paul Dodd - esri   #
#     - Updated to support S3 downloads.          #
#     - Updated to use Verbose.                   #
#     - Updated to use Progress class.            #
#     - Patched FTP logic to support an alternate #
#       query method to retrieve a file's size.   #
# Build: v1.2.0, October 2012, Paul Dodd - esri   #
#     - Updated to include Basic and Digest       #
#       authentication.                           #
#     - Support for secured FTP access.           #
# Build: v1.1.0, September 2012, Paul Dodd - esri #
#     - Updated to support UNC and Local file     #
#       paths for source.                         #
# Build: v1.0.1, August 2012, Paul Dodd - esri    #
#     - Updated to handle cases when RequestInfo  #
#       response has no 'last-modified' property. #
# Build: v1.0.0, May 2012, Paul Dodd - esri       #
###################################################

def getDownload( url, workPath='', timeStamping=True, timeout=30, readSizeKB=8192, authentication=None, userName=None, password=None, verbose=None, headers=None, data=None, sslContext=None):
    """Function: getDownload( <url>[, <workPath>[, <timeStamping>[, <timeout>[, <readSizeKB>[, <authentication>[, <userName>[, <password>[, <verbose>[, <headers>[, <data>[, <sslContext>]]]]]]]]]]])

    Download file from HTTP:, HTTPS:, FTP:, S3:, or FILE: data sources.

    Requires access to 's3cmd.py' for 'S3:' data sources. For details
    please see 'http://s3tools.org/s3cmd'.

    Supports restart of failed FTP and URL transfers!

    Returns:
        True, if local file is successfully updated.
        False, if local file update not required (with timeStamping enabled).
        or an Error exception is raised if trouble is encountered.

    If 'Errno 10013' is received, check your system's advanced Firewall
    permissions settings to ensure that the Python executable is permitted
    access to the Internet.

    Where:
                 <url> = (required) URL, UNC, or File System Path string of file
                         to download. Can be 'Http://...', 'Https://...',
                         'Ftp://...', 'S3://', 'File://...', '\\\\System\\Share\\...',
                         or Local File Path and Name.
            <workPath> = (optional) Path and or filename of output file.
                         Default is current directory with filename of source.
        <timeStamping> = (optional) True, None, False, or datetime.timedelta object.
                         Compare remote file details to local file. Download if
                         file details are different or if details match and
                         <timeStamping> is None. Files are then compared if
                         <timeStamping> is set to None. If <timeStamping> is a
                         datetime.timedelta object, the source file's time stamp is
                         compared to datetime.utcnow - <timeStamping>. If the source
                         is older, a DataError Exception is thrown to that effect.
                         Default is True
             <timeout> = (optional) Number of seconds to wait for content or
                         connection.
                         Default is 30 seconds
          <readSizeKB> = (optional) Size of Read request in KBs. Set to None or
                         0 to use I/O library defaults, 8KB for NON-FTP!
                         Default is 8192KB or 8MB (1KB = 1024 bytes)
      <authentication> = (optional) Authentication URI for user/password if differs
                         from provided url. For HTTP/S connections. Can be specific
                         or partial site URL, as required by host security.
                         Default is None. (ignored by FTP and S3 transfers)
            <userName> = (optional) User name to include in authentication.
                         Default is None. For FTP, default is 'anonymous'.
                         S3 uses default Configuration File. For details please
                         See 'http://s3tools.org/s3cmd' or 's3cmd.py -h'
            <password> = (optional) User password to include in authentication.
                         Default is None. For FTP, default is 'anonymous'.
                         S3 uses default Configuration File. For details please
                         See 'http://s3tools.org/s3cmd' or 's3cmd.py -h'
             <verbose> = (optional) Console display behavior.
                         Default is None (minimal) or value of global
                         verbose (see 'getVerboseHandles' function)
             <headers> = (optional) Dictionary of Key/Value pairs to include in
                         HTTP/S request header. For additional details, see:
                         'http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html'
                         Default is minimal required for transfer.
                <data> = (optional) Dictionary of Key/Value parameter pairs to
                         include in HTTP/S as a POST request. If <data> provided
                         and <url> includes parameters via '?', the parameters
                         are split from the <url> text and added to the <data>.
                         (ignored by FTP and S3 transfers)
                         Default is None, use GET request.
          <sslContext> = (optional) Supported in Python v2.7.9 and above. Supply
                         valid 'ssl.SSLContext' object.
                         Ignored for Python v2.7.8 and below.
                         Default for Python v2.7.12 and below:
                            'ssl.SSLContext( ssl.PROTOCOL_SSLv23)'
                         Default for Python v2.7.13 and above:
                            'ssl.SSLContext( ssl.PROTOCOL_TLS)'
                         For details and additional options, see:
                            https://docs.python.org/library/ssl.html#ssl.SSLContext

    Example Usage:

        import ALFlib

        # Typical download
        if ALFlib.getDownload( "http://my.server.domain/myFolder/myFile.tst"):
            # Do some processing, download was succesful

        # Leverage 'retryIt' function to handle recovery attempts during a transfer failure
        if ALFlib.retyrIt( ALFlib.getDownload, ["http://my.server.domain/myFolder/myFile.zip", "MyFile2.zip"], kwargs={ "timeout": 45}):
            # Do some processing, download was succesful
"""
    # Get verbose handles
    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    def computeRate( lastTime, transferSize):
        # Return Transfer Rate in Size per second

        # Compute time delta then rate
        floatSeconds = getFloatSeconds( datetime.datetime.now() - lastTime)

        if floatSeconds:
            return transferSize / floatSeconds
        else:
            return transferSize

    def computerizeNum( number):
        # Report Tuple containing number converted to Kilo/Mega/Giga bytes, and amount

        if number >= 1073741824:
            # report size in GigaBytes
            divisor = 1073741824
            scale = "GB"
        elif number >= 1048576:
            # report size in MegaBytes
            divisor = 1048576
            scale = "MB"
        else:
            # report size in KiloBytes
            divisor = 1024
            scale = "KB"

        result = float( number) / divisor
        remaindor = result - round( result)

        if not remaindor:
            precision = ""
        elif remaindor < -0.05:
            # Rounded up, so value is less
            precision = "<"
        elif remaindor > 0.05:
            # Rounded down, so value is more
            precision = ">"
        else:
            # Value is a close approximate
            precision = "~"

        return result, scale, precision

    def getFloatSeconds( timeDelta):
        # Return a float of total number of seconds and microseconds

        seconds = float(0)

        if hasattr( timeDelta, 'years'):
            seconds += timeDelta.years * 31536000

        if hasattr( timeDelta, 'weeks'):
            seconds += timeDelta.weeks * 604800

        if hasattr( timeDelta, 'days'):
            seconds += timeDelta.days * 86400

        if hasattr( timeDelta, 'hours'):
            seconds += timeDelta.hours * 3600

        if hasattr( timeDelta, 'minutes'):
            seconds += timeDelta.minutes * 60

        if hasattr( timeDelta, 'seconds'):
            seconds += timeDelta.seconds

        if hasattr( timeDelta, 'microseconds'):
            seconds += float( timeDelta.microseconds) / 10**6

        return seconds

    def formatTime( totalSeconds):
        # Return formatted string of Days, Hours, Minutes, and Seconds from total seconds

        days, totalSeconds = divmod( int( totalSeconds), 86400)
        hours, totalSeconds = divmod( totalSeconds, 3600)
        minutes, totalSeconds = divmod( totalSeconds, 60)

        if days:
            return '{0:02.0f} {1:02.0f}:{2:02.0f}:{3:02.0f}'.format( days, hours, minutes, totalSeconds)
        elif hours:
            return '{0:02.0f}:{1:02.0f}:{2:02.0f}'.format( hours, minutes, totalSeconds)
        else:
            return '{0:02.0f}:{1:02.0f}'.format( minutes, totalSeconds)

    def writeWithFeedback( buffer):
        if isinstance( buffer, float):
            bufferLen = buffer
        elif buffer:
            oFP.write( buffer)
            bufferLen = len( buffer)
        else:
            bufferLen = 0

        ioData['transferSize'] += bufferLen
        ioData['lastSize'] += bufferLen

        if DownloadProgress.willDisplay() or (bufferLen < ioData['readSizeKB']):
            # Only report feedback once a second or when Buffer read doesn't match Request Size
            transferRate = computeRate( ioData['lastTime'], ioData['lastSize'])
            remainingRate = computeRate( ioData['startTime'], ioData['transferSize'])
            if remainingRate:
                timeRemaining = formatTime( float( ioData['requestSize'] - ioData['transferSize']) / remainingRate)
            else:
                timeRemaining = "???"
            comSize = computerizeNum( transferRate)
            if ioData['requestSize']:
                percentComplete = '{0:>4.0f}'.format( (ioData['transferSize'] / ioData['requestSize']) * 100)
            else:
                percentComplete = ' ???'

            elapsedSize = computerizeNum( computeRate( ioData['startTime'], ioData['transferSize']))
            DownloadProgress.display( feedbackString.format(
                percentComplete,
                locale.format_string( '%0.0f', ioData['transferSize'], True),
                locale.format_string( '%0.2f', comSize[0], True),
                comSize[1],
                formatTime( getFloatSeconds( datetime.datetime.now() - ioData['startTime'])),
                locale.format_string( '%0.2f', elapsedSize[0], True),
                elapsedSize[1],
                timeRemaining))
            ioData['lastTime'] = datetime.datetime.now()
            ioData['lastSize'] = 0

    # Invoke Feedback for S3 download
    def s3Feedback( process):
        currentSize = float( os.stat( tempFile).st_size)
        pollSize = currentSize - ioData['lastPollSize']
        writeWithFeedback( pollSize)
        ioData['lastPollSize'] = currentSize
        return (pollSize != 0)	# Report change, resetting download timeout

    def getContext( sslContext):
        # Return Dictionary containing SSL Context based on Python Version
        pyVer = [int(x) for x in platform.python_version().split('.')] + [0, 0] # Need a minimum of 3 values to zip with 'sslOptions'
        sslOptions = [
            [[2,7,13],'ssl.SSLContext(ssl.PROTOCOL_TLS)'],
            [[2,7,9],'ssl.SSLContext(ssl.PROTOCOL_SSLv23)']
            # Ignored for Python < v2.7.9
        ]

        # Take first sslOption where Python version is greater than or equal to specified version
        # NOTE # Use of SSLContext Object is not supported by urllib(2) until Python 2.7.9
        for ver, option in sslOptions:
            for zipper in zip( ver, pyVer):
                if zipper[0] > zipper[1]:
                    break
            else:
                supplied = "Supplied"
                if sslContext and isinstance( sslContext, basestring):
                    try:
                        sslContext = eval( sslContext)
                        supplied = "Derived"
                    except Exception as e:
                        verboseDetail.write( " * Unable to create 'ssl.SSLContext' object from Supplied string, using default!\n   Error: '{0}'\n".format( e))
                        sslContext = None

                if sslContext and not isinstance( sslContext, ssl.SSLContext):
                    verboseDetail.write( " * {0} 'sslContext' object is not of type 'ssl.SSLContext' * Using default!\n".format( supplied))
                    sslContext = None

                verboseDetail.write( " * Setting SSL Context to: '{0}'".format( "User {0} Object".format( supplied) if sslContext else option))
                return { "context": sslContext if sslContext else eval( option)}
        else:
            return {}

    ##############
    # Main logic #
    ##############

    epoch = datetime.datetime.utcfromtimestamp( 0)

    # Set locale, to properly support decimal and group formatting for number display
    if not locale.getlocale()[0]:
        locale.setlocale( locale.LC_ALL, '')

    DownloadProgress = utils.Progress( verbose=verbose)

    # Format source url string to determine protocol
    url = url.replace( "\\", "/")
    protocol = url.split( ":")[0].lower()
    ftpHost = ""
    ftpResource = ""
    request = None
    requestInfo = {}
    ioData = {}

    # Set default SSL Context
    try:
        sslContext = getContext( sslContext)
    except Exception as e:
        verboseDetail.write( '\n * ALFlib.getDownload - Failed to set SSL Context, ignored error: {0}\n'.format( e))
        sslContext = {}

    if protocol not in [ "s3", "http", "https", "ftp"]:
        # Assume protocol is File based

        if not protocol == "file":
            # Get the real path
            url = os.path.realpath( url)

            # Count the leading separators
            seps = url.find( url.lstrip( os.sep))

            if seps >= 2:
                # UNC path
                seps = 2
            else:
                # Local or other
                seps = 3

            url = "file:" + (os.sep * seps) + url.lstrip( os.sep)
            protocol = "file"
    elif protocol == "ftp":
        ftpHost, ftpResource = url[6:].split("/", 1)
        if "@" in ftpHost:
            # User/Password included in URL, extract
            account, ftpHost = ftpHost.split("@", 1)
            if ":" in account:
                userName, password = account.split(":", 1)
            else:
                userName = account
        if not userName:
            userName = "anonymous"
        if not password:
            password = "anonymous@"
    #
    if workPath and not (os.access( workPath, os.F_OK) and os.path.isdir( workPath)):
        # workPath is not a directory (or the directory doesn't exist) assume alternate
        # output file was specified
        workPath, filename = os.path.split( workPath)
    else:
        # v2.3.0, Added split & rstrip
        filename = os.path.split( url.split("?")[0].split("#" if protocol in ["http", "https"] else None)[0].rstrip("/"))[1]

    localFile = os.path.join( workPath, filename)
    localCache = os.path.join( workPath, filename + '.cache')
    tempFile = os.path.join( workPath, '~' + os.path.splitext( filename)[0] + '.tmp')

    verboseCasual.write( "\n--{0}--  '{1}'\n           => '{2}'\n".format(
        datetime.datetime.now().strftime('%H:%M:%S'),
        url,
        localFile))

    try:
        if timeStamping is not False and os.access( localFile, os.F_OK):
            fileModified = datetime.datetime.utcfromtimestamp( os.stat( localFile).st_mtime)
            fileModified -= datetime.timedelta( microseconds=fileModified.microsecond)
        else:
            fileModified = 0

        if ftpHost:
            ftp = ftplib.FTP( ftpHost, userName, password, timeout=timeout)
            if verbose:
                ftp.set_debuglevel(2)
            request, requestInfo['Last-Modified'] = ftp.sendcmd( "MDTM {0}".format( ftpResource)).split()
            try:
                ftp.sendcmd( "TYPE I")  # Set to Binary mode first! v2.1.0
                requestInfo['Content-Length'] = ftp.size( ftpResource)
            except:
                verboseDetail.write( " * SIZE unsupported by Host, trying alternate...\n")

                try:
                    ftpData = []
                    response = ftp.retrlines( "LIST {0}".format( ftpResource), ftpData.append)
                    if not ftpData:
                        raise Exception( "LIST returned no data!")
                    size = ftpData[0].split()
                    if len(size) > 5 and size[-5].isdigit():
                        requestInfo['Content-Length'] = long( size[-5])
                    else:
                        raise Exception( "Unexpected content from LIST command\nResponse: {0}\n    Data: {1}".format( response, ftpData))
                except Exception as e:
                    verboseDetail.write( " * Unable to determine file size...{0}\n".format(e))

            requestInfo['Accept-Ranges'] = "bytes"
            requestInfo['Content-Type'] = "application/" + ftpResource.split(".")[-1:][0]
        elif protocol == "s3":
            if not hasattr( utils, "s3"):
                utils.s3 = utils.S3cmd( verbose=(verbose == True))
            request = utils.s3.getInfo( bucketPath=url, verbose=(verbose == True))
            if request:
                requestInfo['Last-Modified'] = request.lastModified
                requestInfo['Content-Length'] = request.size
                requestInfo['Content-Type'] = request.mimeType
            else:
                raise urllib2.HTTPError( url, 404, "Not Found", None, None)
        else:
            urlData = {}

            # Check for and use supplied 'data' Dictionary is available
            if data:
                if not isinstance( data, dict):
                    verboseDetail.write( " * Ignoring provided 'data', not a valid Dictionary! *\n")
                else:
                    urlData = data

            # Add URL parameters to data, key=value pairs to right of '?'
            urlParameters = url.split("?", 1)
            if urlData and len( urlParameters) > 1 and urlParameters[-1]:
                # We have Parameters!
                for pair in urlParameters[-1].split("&"):
                    if "=" in pair:
                        key, value = pair.split("=", 1)
                        if key not in urlData:
                            # Store parameter and value in data
                            urlData[key] = value

                # Reset URL to text Left of '?'
                url = urlParameters[0]

            # Add Cookie Jar
            cj = cookielib.CookieJar()
            authHandlers = []

            # Add Password Manager
            if userName or password:
                uri = url[0:(url+"/").index("/",8)].split("//")[1]  # Specify authentication uri based on URL
                if authentication and authentication not in ["basic", "digest"]: # ignore if includes past version specifications
                    uri = authentication    # Specify authentication uri based on provided uri

                verboseDetail.write( " * Authenticating user to: '{0}'\n".format( uri))

                pwMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                pwMgr.add_password(realm=None,
                                uri=uri,
                                user=userName,
                                passwd=password)

                authHandlers.append( urllib2.HTTPBasicAuthHandler( pwMgr))
                authHandlers.append( urllib2.HTTPDigestAuthHandler( pwMgr))

            # Add SSL handler
            if sslContext:
                authHandlers.append( urllib2.HTTPSHandler( ** sslContext))

            # Add Cookie Handler
            authHandlers.append( urllib2.HTTPCookieProcessor(cj))

            urllib2.install_opener( urllib2.build_opener( * authHandlers))

            if urlData:
                # Url Encode data
                urlData = urllib.urlencode( urlData)
            else:
                urlData = None

            if not isinstance( headers, dict):
                headers = {}

            if timeStamping and fileModified:
                # Only allow if timeStamping is True!
                headers[ "If-Modified-Since"] = fileModified.strftime( "%a, %d %b %Y %H:%M:%S GMT")

                # Add stored cache control headers if present
                try:
                    if os.access( localCache, os.F_OK):
                        with open( localCache, "r") as iFP:
                            jsonData = json.load( iFP)
                            for key, value in jsonData.iteritems():
                                headers[ key] = value

                except Exception as e:
                    verboseCasual.write( "\n * 'getDownload' issue loading cache file: {0}\n".format( e))

            # Add User Agent to header, if needed
            for key in headers:
                if key.lower() == "user-agent":
                    break
            else:
                headers[ "User-Agent"] = "Python/v{0} ALFlib.py/v{1}.{2}.{3}".format( platform.python_version(), utils.major, utils.minor, utils.bug)

            # Report request
            if verbose:
                verboseDetail.write( "\nRequest Headers: \n")

                for key, value in headers.iteritems():
                    verboseDetail.write( " - {0}: {1}\n".format( key, value))

                # Report data
                if urlData:
                    verboseDetail.write( "\nRequest Data: \n")

                    for pair in urlData.split("&"):
                        if "=" in pair:
                            key, value = pair.split("=", 1)
                            verboseDetail.write( " - {0}={1}\n".format( key, "******" if key.lower() == "password" else value))

            # Get results
            request = urllib2.urlopen( urllib2.Request( url, urlData, headers), timeout=timeout)#, ** sslContext)
            requestInfo = request.info()

            # Report results
            if verbose:
                verboseDetail.write( "\nResponse Info:\n".format( requestInfo))
                for key, value in request.info().dict.iteritems():
                    verboseDetail.write( " - {0}: {1}\n".format( key, value))

    except urllib2.HTTPError as e:
        if e.code == 304:
            if isinstance( timeStamping, datetime.timedelta) and fileModified:
                if fileModified <= (datetime.datetime.utcnow() - timeStamping):
                    raise DataError( "Remote file is Stale, it has not changed since: {0}".format( fileModified))

            verboseCasual.write( "\n * Remote file is older than Local or has not change -- NOT retrieving.\n")
            return
        raise
    except ftplib.error_perm as e:
        code = int( str(e).split()[0])
        if code == 550:
            raise ftplib.error_perm( "550 Permission Denied, or No such file or folder")
    except:
        verboseCasual.write( " * Failed to access URL: {0}\n".format( sys.exc_info()[0]))
        raise

    ioData['lastSize'] = float(0)
    ioData['lastTime'] = None
    ioData['lastPollSize'] = float(0)
    ioData['startTime'] = None
    ioData['transferSize'] = float(0)
    ioData['requestSize'] = 0
    ioData['readSizeKB'] = readSizeKB

    restartable = ()
    restart = 0

    if request and requestInfo:
        if 'Last-Modified' in requestInfo:
            if ftpHost:
                requestModified = datetime.datetime.strptime( requestInfo['Last-Modified'], '%Y%m%d%H%M%S')
            elif protocol == "s3":
                requestModified = requestInfo['Last-Modified']
            else:
                requestModified = datetime.datetime.strptime( requestInfo['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')
        else:
            requestModified = "* * * Unknown * * *"
            #requestModified = datetime.datetime.utcnow()
            #requestModified -= datetime.timedelta( microseconds=requestModified.microsecond)

        if 'Content-Type' in requestInfo:
            requestType = requestInfo['Content-Type']
        else:
            requestType = 'Unknown'

        if 'Content-Length' in requestInfo:
            ioData['requestSize'] = long( requestInfo['Content-Length'])
        else:
            ioData['requestSize'] = 0

        if isinstance( requestModified, datetime.datetime):
            # Calc Time Delta of file using Epoch, then compute UTC Total Seconds
            td = requestModified - epoch
            requestTime = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        else:
            requestTime = 0

        # Configure restart download details
        if 'Accept-Ranges' in requestInfo and 'Content-Length' in requestInfo and 'Last-Modified' in requestInfo:
            restartable = (requestTime, ioData['requestSize'])
            tempFile = "{0}.{1}_{2}.tmp".format( os.path.splitext( tempFile)[0], * restartable)
    else:
        raise Exception( " * Unknown URL response *\n Request Obj = '{0}'\nRequest Info = '{1}'\n".format( request, requestInfo))

    verboseCasual.write( "\n        Last Modified (UTC) -       Size       Restartable  Type\n")
    comSize = computerizeNum( ioData['requestSize'])
    verboseCasual.write( "Remote: {0} - {1} ({2}{3:0.0f} {4})   {6}   [{5}]\n".format(
        requestModified,
        locale.format_string( '%0.0f', ioData['requestSize'], True),
        comSize[2],
        comSize[0],
        comSize[1],
        requestType,
        "Yes" if restartable else "No "))

    if restartable and os.access( tempFile, os.F_OK):
        restart = os.stat( tempFile).st_size
        if restart:
            # Don't 'restart' if at zero
            ioData['transferSize'] = float( restart)
            verboseCasual.write( "\n * Restarting previous download from byte: {0} *\n".format( restart))

    elif timeStamping is not False and os.access( localFile, os.F_OK):
        fileSize = os.stat( localFile).st_size
        comSize = computerizeNum( fileSize)
        verboseCasual.write( " Local: {0} - {1} ({2}{3:0.0f} {4})\n".format(
            fileModified,
            locale.format_string( '%0.0f', fileSize, True),
            comSize[2],
            comSize[0],
            comSize[1]))

        # Check for Cache Control content in response
        try:
            cacheControl = {}
            if "dict" in requestInfo:
                for key, value in requestInfo.dict.iteritems():
                    if key.lower() == "etag":
                        cacheControl[ "If-None-Match"] = value
                        cacheControl[ "Cache-Control"] = "max-age=0"

            # Save/Remove control content
            if cacheControl:
                # Update cache
                with open( localCache, "w") as oFP:
                    json.dump( cacheControl, oFP, indent=3, separators=(",", ": "))
            elif os.access( localCache, os.F_OK):
                # Clear cache
                os.remove( localCache)

        except Exception as e:
            verboseCasual.write( "\n * 'getDownload' issue saving/clearing cache file: {0}\n".format( e))

        # Ok to download based on timestamp?
        if requestTime:
            if isinstance( timeStamping, datetime.timedelta):
                if requestModified <= (datetime.datetime.utcnow() - timeStamping):
                    raise DataError( "Remote file is Stale, it has not changed since: {0}".format( requestModified))

            if requestModified > fileModified:
                verboseCasual.write( "\n * Remote file is newer than local -- retrieving.\n")
                timeStamping = True # Override file compare later on, no need to do it now.
            elif requestModified < fileModified:
                verboseCasual.write( "\n * Remote file is older than local -- NOT retrieving.\n")
                return
            else:
                requestModified = None

        # Check if
        if not isinstance( requestModified, datetime.datetime):
            if ioData['requestSize'] != fileSize:
                if ioData['requestSize']:
                    verboseCasual.write( "\n * Local file size does not match remote -- retrieving.\n")
                    timeStamping = True # Override file compare later on, no need to do it now.
                else:
                    verboseCasual.write( "\n * Remote file size is unknown -- must retrieve and compare!\n")
                    timeStamping = None # Enable file compare later on
            elif timeStamping is None:
                verboseCasual.write( "\n * Local file details match remote -- must retrieve and compare!\n")
            else:
                verboseCasual.write( "\n * Remote file size matches local -- NOT retrieving.\n")
                return

    verboseCasual.write( "\nWriting: '{0}'\n".format( localFile))

    try:
        if restart:
            oFP = open( tempFile, 'ab') # Append to existing temp file
        else:
            oFP = open( tempFile, 'wb') # Create/overwrite temp file

    except:
        verboseDetail.write( " * Failed to create temporary output '{0}': {1}\n".format( tempFile, sys.exc_info()[0]))
        raise

    ioData['startTime'] = datetime.datetime.now()

    if ioData['readSizeKB']:
        ioData['readSizeKB'] *= 1024
    elif ftpHost:
        ioData['readSizeKB'] = 0    # Default to I/O library
    else:
        ioData['readSizeKB'] = 8192 # Default to 8KB

    feedbackString = "{0}% {1:>" + str(len( locale.format_string( '%0.0f', ioData['requestSize'], True))) + "} {2:>8}{3}/s ({4} @ {5}{6}/s) ETA({7})"
    buffer = True
    error = None

    try:
        ioData['lastTime'] = datetime.datetime.now()

        if ftpHost:
            try:
                if restart:
                    # Manually send RESTart command with added newline. Some sites fail to allow restarts without it!
                    try:
                        ftp.sendcmd( 'REST {}\n'.format( restart))
                    except:
                        ftp.sendcmd( 'REST {}'.format( restart))
                if ioData['readSizeKB']:
                    ftp.retrbinary( "RETR {0}".format( ftpResource), writeWithFeedback, ioData['readSizeKB']) #, rest=restart)
                else:
                    ftp.retrbinary( "RETR {0}".format( ftpResource), writeWithFeedback) #, rest=restart)

            except ftplib.error_reply as e:
            #except Exception as e:
                if restart:
                    verboseCasual.write( "\n * Unable to restart download, starting over *\n")
                    oFP = open( tempFile, 'wb') # Create/overwrite temp file
                    ioData['transferSize'] = 0.0
                    if ioData['readSizeKB']:
                        ftp.retrbinary( "RETR {0}".format( ftpResource), writeWithFeedback, ioData['readSizeKB'])
                    else:
                        ftp.retrbinary( "RETR {0}".format( ftpResource), writeWithFeedback)
                else:
                    raise

            finally:
                ftp.close()

        elif protocol == "s3":
            # Download from S3 and only show Casual detail when Verbose is True
            utils.s3.getFile( bucketPath=url, destination=tempFile, callOptions=['--force'], timeout=timeout, timerHook=s3Feedback, verbose=(verbose == True))
        else:
            if restart:
                headers[ "Range"] = "bytes={0}-".format( restart)
                request = urllib2.urlopen( urllib2.Request( url, urlData, headers), timeout=timeout, ** sslContext)

            bufferSize = ioData['readSizeKB']

            while buffer:
                buffer = request.read( bufferSize)
                writeWithFeedback( buffer)

    except KeyboardInterrupt as e:
        error = Exception( "Keyboard Interrupt detected")

    except Exception as e:
        error = e

    finally:
        if not oFP.closed:
            try:
                oFP.flush()
            except:
                pass
            oFP.close()

        try:
            # Close request if open
            request.close()
        except:
            pass

        transferRate = computeRate( ioData['startTime'], ioData['transferSize'])
        comSize = computerizeNum( transferRate)
        DownloadProgress.clear( "{0} ({1} @ {2} {3}/s) - Saved [{4}/{5}]".format(
            datetime.datetime.now().strftime('%H:%M:%S'),
            formatTime( getFloatSeconds( datetime.datetime.now() - ioData['startTime'])),
            locale.format_string( '%0.2f', comSize[0], True),
            comSize[1],
            long( ioData['transferSize']),
            ioData['requestSize']))

        if error:
            verboseCasual.write( "\n * Failed to complete transfer of file '{0}': {1}\n".format( localFile, sys.exc_info()[0]))

        if requestTime:
            # Set date time of file
            os.utime( tempFile, ( requestTime, requestTime))

        # v1.4.1 update - added 'and not error'
        if (long( ioData['transferSize']) >= ioData['requestSize']) and not error:
            if os.access( localFile, os.F_OK):
                if timeStamping is None and filecmp.cmp( tempFile, localFile):
                    verboseCasual.write( "\n * Remote file matches local -- Download discarded!\n")
                    os.remove( tempFile)
                    return False
                os.remove( localFile)
            os.rename( tempFile, localFile)

            # Removal all remaining temp files that match this download
            for item in utils.iterPath( workPath if workPath else '.', '~' + os.path.splitext( filename)[0] + ".*tmp", recurse=False):
                try:
                    os.remove( item)
                except:
                    pass

            return True
        else:
            if not restartable:
                os.remove( tempFile)
            else:
                verboseCasual.write( "\n * Download is Restartable!\n")

            if error:
                raise error
            else:
                raise Exception( "Size of download does not match source!")

########################################################
# Get Internal and External Network Details about Host #
#                                                      #
# Build: v1.0.0, May 2014, Paul Dodd - esri            #
########################################################

def getNetworkDetails( flushCache=False, verbose=None):
    """Function: getNetworkDetails( [<flushCache>[, <verbose>]])

    Get the internal and external Network details about this Host machine.
    External details are supplied by accessing 'http://icanhazip.com'.
    For more info see: 'http://major.io/icanhazip-com-faq/'

    Where:
        <flushCache> = (optional) True or False whether or not to re-create
                       the cache file stored in the system or user Temp folder.
                       If True; or when the cache file does NOT exist; or when
                       the Local Host Name or IP differs from the cache, the
                       external Host Name and IP values are requested from the
                       icanhazip web end-points and stored in the cache file.
                       If False, no external web requests are made, details are
                       simply retrieved, if available, from the cache file.
                       Default is False

           <verbose> = (optional) Console display behavior.
                       Default is None (minimal) or value of global
                       verbose (see 'getVerboseHandles' function)

    Returns a cached Dictionary that includes the following content:

    {
           "localName": <Local Host and Domain name of machine>,
         "localDomain": <Local Domain name for machine>,
           "localAddr": <Local IP Address of machine>,
        "externalName": <External DNS name of machine>,
        "externalAddr": <External IP Address of machine>
    }

    If an error condition is encountered, the details will also include:
        "error": <exception object>
"""
    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    def findDomain( hostname):
        # Enlist 'nslookup' to identify SOA server details, then extact Domain name and return
        outcome, reply = utils.callCommandLine( ["nslookup", "-type=SOA", hostname], verbose=verbose)

        if outcome:
            verboseDetail.write( "\n * 'getNetworkDetails' was unable to: Find Host Domain, outcome: '{0}', reply: '{1}'\n".format( outcome, reply))
        else:
            lastLine = ""
            for line in reply:
                if "origin" in line or "primary name server" in line:
                    domain = line.split()[-1]
                    if lastLine in domain:
                        return unicode( lastLine)
                    return unicode( domain.split(".", 1)[-1])

                # Save line content for next comparison
                lastLine = line.strip()

        # No Domain found...
        return u""

    def getExternal( url, desc, errors):
        try:
            return urllib2.urlopen( url, timeout=5).readline().strip()

        except Exception as e:
            verboseDetail.write( "\n * 'ALFlib.getNetworkDetails' was unable to: {0}: {1}\n".format( desc, e))
            errors[ desc] = "{0}".format( e)

        return ""

    scriptName = os.path.split( __file__)[-1]
    fileName = os.path.join( tempfile.gettempdir(), "{0}_{1}".format( scriptName.split( ".")[0], "NetworkDetails.json"))

    localName = unicode( socket.getfqdn().capitalize())
    localDomain = localName.split( ".", 1)[-1]
    localAddr = u""
    try:
        # Try to locate address using fully qualified machine name
        localAddr = unicode( socket.gethostbyname( localName))
    except:
        try:
            # Fallback to locating address without using the domain
            localAddr = unicode( socket.gethostbyname( localName.split( ".")[0]))
        except:
            pass

    details = { u"localName": u"", u"localDomain": u"", u"localAddr": u"", u"externalName": u"", u"externalAddr": u""}
    errors = {}

    try:
        if not flushCache:
            if hasattr( utils, "_NetworkDetails"):
                if not verbose == False:
                    # Only record action if not explicitly told not to
                    verboseDetail.write( "\n - 'getNetworkDetails' Hydrate from cache Details...\n")
                details = getattr( utils, "_NetworkDetails")
            elif os.path.exists( fileName):
                # Hydrate details from file
                if not verbose == False:
                    # Only record action if not explicitly told not to
                    verboseDetail.write( "\n - 'getNetworkDetails' Hydrate from cache File: '{0}'\n".format( fileName))
                with open( fileName, "r") as iFP:
                    details = json.load( iFP)
                    setattr( utils, "_NetworkDetails", details)

        if details.get( u"localName", u"") != localName or u"localDomain" not in details or details.get( u"localAddr", u"") != localAddr:
            if localName == localDomain:
                localDomain = findDomain( localName)

            details = { u"localName": localName, u"localDomain": localDomain, u"localAddr": localAddr}

            if not verbose == False:
                # Only record action if not explicitly told not to
                verboseDetail.write( "\n - 'getNetworkDetails' Hydrate and Cache from Internet...\n")

            # Get external name and IP
            extAddr = getExternal( "http://www.icanhazip.com", "Get External Address", errors)
            extName = getExternal( "http://www.icanhazptr.com", "Get External Name", errors)

            if errors:
                details[ "error"] = errors

            # Verify details
            if extName == extAddr:
                unknown = " * Unknown * "
                # Check for IPv4 and IPv6 address in name
                if not extName:
                    extName = unknown
                    extAddr = unknown
                elif extName.replace( ".", "").isdigit() or ":" in extName:
                    extName = unknown
                else:
                    extAddr = unknown

            details[ u"externalAddr"] = unicode( extAddr)
            details[ u"externalName"] = unicode( extName)

            # Save details to local ALFlib
            setattr( utils, "_NetworkDetails", details)
            # Save details to disk file
            with open( fileName, "w") as oFP:
                json.dump( details, oFP, indent=3, separators=(",", ": "))

    except Exception as e:
        verboseDetail.write( "\n * 'ALFlib.getNetworkDetails' was unable to perform function: {0}\n".format( e))
        errors[ "General Error"] = "{0}".format( e)

    finally:
        if errors:
            details[ "error"] = errors

    return details

#################################################
# Normalize XML content for easy use in Python  #
#                                               #
# Build: v1.0.0, Jun 2012, Paul Dodd - esri     #
#################################################

def xmlNormalizer( node):
    """Function: xmlNormalizer( <node>)

    Turns XML content into a more Python friendly 'normalized' structure.

    Returns:
        An 'ALFlib.OrderedDict' object containing XML Elements and Attributes
        stored as 'dot notation' or '[<item>]' or '[<index>]' accessible
        Dictionaries and Lists that are Iterable.

    Where:
        <node> = (required) A valid 'xml.dom.Document' or 'xml.dom.Node' object.

    Behavior:
        XML Elements are stored as a Property (or attributes) named after the
        Element. Like: '<object>.<ElementName>'

        XML Elements that are repeated are stored as an Iterable List Property
        named after the Element. Like: '<object>.<ElementName>[]'

        XML Element Attributes are stored within the Element Property as a List
        Property named 'attributes'. Like: '<object>.<ElementName>.attributes[]'

        XML Element 'Text' is stored within the Element Property as a Property
        (or List if repeated) named 'text'.
        Like: '<object>.<ElementName>.text' or '<object>.<ElementName>.text[]'

        XML Element 'Comment' is stored within the Element Property as a
        Property (or List if repeated) named 'comment'.
        Like: '<object>.<ElementName>.comment' or
              '<object>.<Elementname>.comment[]'

        Other content, like 'CDATA' values, will also be turned into Element
        Properties. Like: '<object>.<ElementName>["cdata-section"]' * Note that
        these are NOT 'dot notation' accessible!

    'RSS' Example:

        <?xml version="1.0" encoding="UTF-8" ?>
            <rss version="2.0">
                <channel>
                    <title>RSS Title</title>
                    <description>This is an example of an RSS feed</description>
                    <link>http://www.someexamplerssdomain.com/main.html</link>
                    <lastBuildDate>Mon, 06 Sep 2010 00:01:00 +0000 </lastBuildDate>
                    <pubDate>Mon, 06 Sep 2009 16:45:00 +0000 </pubDate>
                    <ttl>1800</ttl>

                    <item>
                        <title>Example entry</title>
                        <description>An interesting description.</description>
                        <link>http://www.wikipedia.org/</link>
                        <guid>unique string per item</guid>
                        <pubDate>Mon, 06 Sep 2009 16:45:00 +0000 </pubDate>
                    </item>

                    <item>
                        ...
                    </item>
                </channel>
            </rss>

        Which produces:

        <ALFlib.OrderedDict> object with the following Properties:
         |- text = None
         |- comment = None
         |- attributes[]
         \- rss
             |- text = None
             |- comment = None
             |- attributes[0]
             |   \- version = '2.0'
             \- channel
                 |- text = None
                 |- comment = None
                 |- attributes[]
                 |- title
                 |   |- text = 'RSS Title'
                 |   |- comment = None
                 |   \- attributes[]
                 |- description
                 |   |- text = 'This is an example of an RSS feed'
                 |   |- comment = None
                 |   \- attributes[]
                 |- link
                 |   |- text = 'http://www.someexamplerssdomain.com/main.html'
                 |   |- comment = None
                 |   \- attributes[]
                 |- lastBuildDate
                 |   |- text = 'Mon, 06 Sep 2010 00:01:00 +0000 '
                 |   |- comment = None
                 |   \- attributes[]
                 |- pubDate
                 |   |- text = 'Mon, 06 Sep 2009 16:45:00 +0000 '
                 |   |- comment = None
                 |   \- attributes[]
                 |- ttl
                 |   |- text = '1800'
                 |   |- comment = None
                 |   \- attributes[]
                 |- item[0]
                 |   |- text = None
                 |   |- comment = None
                 |   |- attributes[]
                 |   |- title
                 |   |   |- text = 'Example entry'
                 |   |   |- comment = None
                 |   |   \- attributes[]
                 |   |- description
                 |   |   |- text = 'An interesting description.'
                 |   |   |- comment = None
                 |   |   \- attributes[]
                 |   |- link
                 |   |   |- text = 'http://www.wikipedia.org/'
                 |   |   |- comment = None
                 |   |   \- attributes[]
                 |   |- guid
                 |   |   |- text = 'unique string per item'
                 |   |   |- comment = None
                 |   |   \- attributes[]
                 |   \- pubDate
                 |       |- text = 'Mon, 06 Sep 2009 16:45:00 +0000 '
                 |       |- comment = None
                 |       \- attributes[]
                 \- item[n]
                     |- text = None
                     |- comment = None
                     |- attributes[]
                     \- ???

    Example Usage:

        # Read XML from URL and display 'title' text from each item

        from xml.dom.minidom import parse
        from urllib2 import urlopen
        from ALFlib import xmlNormalizer

        xmlSource = urlopen( 'http://My.server.com/MyRssFeed.xml')
        xmlDoc = parse( xmlSource)
        xml = xmlNormalizer( xmlDoc)

        for item in xml.rss.channel.item:
            print item.title.text
"""
    data = utils.OrderedDict()
    data[ u'attributes'] = utils.OrderedDict()
    data[ u'text'] = None
    data[ u'comment'] = None

    if hasattr( node, u'attributes') and node.attributes:
        for index in range(0, node.attributes.length, 1):
            attribute = node.attributes.item( index)
            data.attributes[ attribute.nodeName] = attribute.nodeValue

    for child in node.childNodes:
        if child.nodeName.startswith( '#'):
            nodeName = unicode( child.nodeName[1:])
        else:
            nodeName = unicode( child.nodeName)

        if isinstance( child.childNodes, list):
            newData = xmlNormalizer( child)
        else:
            newData = child.nodeValue

        if hasattr( data, nodeName) and data[ nodeName] != None:
            if not isinstance( data[ nodeName], list):
                data[ nodeName] = [ data[ nodeName]]
            data[ nodeName].append( newData)
        else:
            data[ nodeName] = newData

    return data

######################################################
# Check availability of 7Zip pack/unpack routine     #
#                                                    #
# Build: v1.0.0, Sep 2012, Paul Dodd - esri          #
######################################################

def check7zip( retry=False, verboseHandle=None):
    """Function: check7zip( [<retry>[, <verboseHandle>]])

    Check (and cache) the availability of the 7zip pack/unpack tool.

    Returns:
        True or 7zip version string, when initial or prior check for 7Zip tool
                                     was successful.
         None = Initial or <retry> failed to find 7Zip tool.
        False = Prior (cached) check failed to find 7Zip tool.

    Where:
                <retry> = (optional) Set to True to ignore last cached result
                          and re-check for 7zip routine.
        <verboseHandle> = (optional) Provide a File handle of where to write
                          messages to if needed. Could be handle from
                          'getVerboseHandles' routine.
                          Default is sys.stderr handle
"""

    if retry or not hasattr( utils, 'found7zip'):
        if not isinstance( verboseHandle, file):
            verboseHandle = sys.stderr	# Default to Standard Error

        utils.found7zip = None	# Set to None first time through

        try:
            verboseHandle.write( "  Checking for 7zip tool...")

            outcome, console = utils.callCommandLine( ["7z"])
            if outcome == 0:
                for line in console:
                    if line.startswith( "7-Zip"):
                        utils.found7zip = line.split()[2]
                        if utils.found7zip.find(".") == 1:
                            utils.found7zip = " {0}".format( utils.found7zip)
                        break
                else:
                    utils.found7zip = True
                verboseHandle.write( "Found\n")

        except Exception as e:
            outcome = e

        if outcome:
            verboseHandle.write( "Unavailable!\n")
            verboseHandle.write( " * Outcome or Error: {0}\n".format( outcome))

    elif not utils.found7zip:
        utils.found7zip = False

    return utils.found7zip

######################################################
# unZip archive routine. Uses 7Zip or Python zipfile #
# logic to unpack zipped content.                    #
#                                                    #
# Build: v1.3.0, Mar 2017, Paul Dodd - esri          #
#      - Added 'inclusions', 'exclusions', and       #
#        'recurse' options.                          #
# Build: v1.2.0, Feb 2014, Paul Dodd - esri          #
#      - Altered to return list of files extracted.  #
# Build: v1.1.1, May 2012, Paul Dodd - esri          #
#      - Altered not to include 7zip '-p' option     #
#        when password not specified.                #
# Build: v1.1.0, Apr 2012, Paul Dodd - esri          #
#      - Updated to take advantage of 'maskPassword' #
#        option in 'callCommandLine' routine.        #
# Build: v1.0.0, Nov 2012, Paul Dodd - esri          #
######################################################

def unzipIt( zipFile, destination=None, password=None, verbose=None, inclusions=[], exclusions=[], recurse=True):

    """Function: unzipIt( <zipFile>[, <destination>[, <password>[, <verbose>[, <inclusions>[, <exclusions>[, <recurse>]]]]])

    Unpack contents of a Zip or other archive file using the 7zip pack/unpack
    tool or the built in (but slower - for Zip archives only!) Python zipfile
    routine. Unpacking Non-Zip files is only available when 7zip routine is
    installed and accessible via system path.

    Returns:
         List = Containing string path names of all files extracted if successful.
           [] = If one or more files fail to extract.

    Exception is raised if a more serious issue is detected!

    Where:
            <zipFile> = Filename and optional Path to Zip File that will be
                        unpacked.
        <destination> = (optional) Path to existing folder where files will be
                        placed.
                        Default is current directory.
           <password> = (optional) Password to use to unpack content.
                        Default is no password.
            <verbose> = (optional) Console display behavior.
                        Default is None (minimal) or value of global
                        verbose (see 'getVerboseHandles' function)
         <inclusions> = (optional) String or List of Strings containing name
                        of or wildcards for content to extract. See <source>
                        Default is an Empty List (nothing)
         <exclusions> = (optional) String or List of Strings containing
                        name of or wildcards for content NOT to extract.
                        Default is an Empty List (nothing)
            <recurse> = (optional) True or False. Specify whether or not
                        to recursively extract directory contents.
                        Default is True, extract all files!
"""
    # Get verbose handles
    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    if not password:
        password = ""
    if not destination:
        destination = "."
    if not inclusions:
        inclusions = []
    elif not isinstance( inclusions, list):	# Allow for multiple inclusions
        inclusions = [ "{0}".format( inclusions)]
    if not exclusions:
        exclusions = []
    elif not isinstance( exclusions, list):	# Allow for multiple exclusions
        exclusions = [ "{0}".format( exclusions)]

    if not os.access( zipFile, os.F_OK):
        raise Exception( "\n * Unable to access archive '{0}' *".format( zipFile))
    if not os.access( destination, os.W_OK):
        raise Exception( "\n * Unable to write to destination '{0}' *".format( destination))

    # Check for 7Zip tool
    version7zip = utils.check7zip( verboseHandle=verboseCasual)
    if version7zip == None:
        verboseDetail.write( "\n * Falling back to internal (slower) Python unzip process! *\n")
        verboseCasual.write( " * 7Zip unavailable, using (slower) Python unzip process!\n")

    # Prep for extract
    callOptions = [
        "7z",
        "x",
        #"-r",
        "-y"
    ]

    if recurse:
        callOptions.append( "-r")
    elif not inclusions and not exclusions:
        inclusions = ["*.*"]

    bb7zip = False
    if isinstance( version7zip, basestring) and version7zip >= "15.05":
        # Add option to raise logging level, to show files being exported
        callOptions.append( "-bb1")
        bb7zip = True

    maskPassword = False
    if password:
        # Include 'maskPassword' text around password for display!
        callOptions.append( "-p\*" + password + "\*")
        maskPassword = True
    else:
        # Include dummy Password to avoid 7zip asking for a password!
        callOptions.append( "-p.")

    callOptions.append( "-o" + destination)

    # Add inclusions
    for item in inclusions:
        callOptions.append( "-i!" + item)

    # Add exclusions
    for item in exclusions:
        callOptions.append( "-x!" + item)

    callOptions.append( zipFile)

    ZipFile = None
    outcome = None
    members = []

    try:
        verboseCasual.write( "  Extracting...")

        if version7zip:
            outcome, results = utils.callCommandLine( callOptions, verbose=(verbose == True), maskPassword=maskPassword)
            if outcome in [0, 1]:
                for line in results:
                    member = []
                    if bb7zip or line.startswith( "- "):
                        # Version 15.05 or newer!
                        member = line.split( " ", 1)
                    else:
                        member = line.split( "  ", 1)

                    if len( member) > 1 and member[0] in ["Extracting", "-"]:
                        member = os.path.join( destination, member[1].strip())
                        if os.path.isfile( member):
                            members.append( member)
        else:
            fnFunc = fnmatch.fnmatch
            ZipFile = zipfile.ZipFile( zipFile, "r")
            if password:
                ZipFile.setpassword( password)

            # Collect items to be extracted
            infoList = ZipFile.infolist()

            if not infoList:
                verboseCasual.write( " * Nothing to extract, archive is empty! *\n")
            else:
                folders = 0
                files = 0
                compressed = os.stat( zipFile).st_size
                size = 0
                # Extract from list of members
                verboseDetail.write( "\nUsing Python zipfile object\n")
                verboseDetail.write( "\nProcessing archive: {0}\n\n".format( zipFile.replace( "/", os.sep)))
                for info in infoList:
                    member = info.filename
                    if not recurse and os.path.split( member)[0]:
                        continue

                    exclude = False
                    for exclusion in exclusions:
                        if fnFunc( member, exclusion):
                            exclude = True
                            break
                    if exclude:
                        continue

                    if inclusions:
                        include = False
                        for inclusion in inclusions:
                            if fnFunc( member, inclusion):
                                include = True
                                break
                        if not include:
                            continue

                    size += info.file_size
                    sys.stdout.write( ".")
                    verboseDetail.write( "Extracting  {0}\n".format( member.rstrip("/").replace( "/", os.sep)))
                    ZipFile.extract( member, destination)

                    if member.endswith("/"):
                        folders += 1
                    else:
                        members.append( os.path.join( destination, member))
                        files += 1
                outcome = 0
                verboseDetail.write( "\nEverything is Ok\n")
                verboseDetail.write( "\nFolders: {0}".format( folders))
                verboseDetail.write( "\nFiles: {0}".format( files))
                verboseDetail.write( "\nSize:       {0}".format( size))
                verboseDetail.write( "\nCompressed: {0}\n".format( compressed))

    except Exception as e:
        outcome = e

    if ZipFile:
        ZipFile.close()

    if outcome == 0:
        verboseCasual.write( "Success\n")
    elif outcome == 1:
        verboseCasual.write( " * Caution * Outcome: 1, some files may not have been uncompressed!\n")
    elif outcome == 7:
        raise Exception( "Outcome: 7, input error, review details")
    elif outcome == 8:
        raise Exception( "Outcome: 8, insufficient memory, review details")
    else:
        raise Exception( "Fatal Error! Outcome: {0}, review details".format( outcome))

    if outcome == 0:
        return members

    return []

######################################################
# Zip archive routine. Uses 7Zip or Python zipfile   #
# logic to pack content in a zip archive.            #
#                                                    #
# Build: v1.2.0, Apr 2015, Paul Dodd - esri          #
#      - Updated to leverage 'iterPath' function.    #
# Build: v1.1.2, Dec 2013, Paul Dodd - esri          #
#      - Patched inclusion and exclusion to include  #
#        recursive option 'r'.                       #
# Build: v1.1.1, May 2012, Paul Dodd - esri          #
#      - Altered not to include 7zip '-p' option     #
#        when password not specified.                #
# Build: v1.1.0, Apr 2012, Paul Dodd - esri          #
#      - Updated to take advantage of 'maskPassword' #
#        option in 'callCommandLine' routine.        #
# Build: v1.0.0, Jan 2013, Paul Dodd - esri          #
######################################################

def zipIt( source, zipFile, append=False, recurse=None, useCompression=True, inclusions=[], exclusions=[], password=None, verbose=None):

    """Function: zipIt( <source>, <zipFile>[, <append>[, <recurse>[, <useCompression>[, <inclusions>[, <exclusions>[, <password>[, <verbose>]]]]]]])

    Archive specified content to a Zip or other archive file using the 7zip
    pack/unpack tool or the built in (but slower - Zip archives only!) Python
    zipfile routine. Creating Non-Zip archives is only available when 7zip
    routine is installed and accessible via system path.

    Returns:
         True = If successful.
        False = If one or more files fail to archive.

    Exception is raised if a more serious issue is detected!

    Where:
                <source> = String or List of Strings containing name of or
                           wildcards for content to archive.
                           - If directory is specified without specific
                           content or wildcard, the directory contents will
                           be archived using recursion (regardless of the
                           recurse setting) including the root directory
                           name.
                           - In all other cases, matching content is
                           archived without the root directory name.
                           - To recursively archive a directory without
                           including the root directory name, use '*.*'
                           wildcard and set recurse=True.
               <zipFile> = Filename and optional Path to archive file that
                           will be created or appended to.
                <append> = (optional) True or False. Specify whether or not
                           to append to an existing archive.
                           Default is False (overwrite if file exists)
               <recurse> = (optional) True or False. Specify whether or not
                           to recursively archive a directory's contents.
                           Default is False (True for each <source> that is a
                           directory)
        <useCompression> = (optional) True or False. Specify whether or not to
                           use compression when archiving files.
                           Default is True
            <inclusions> = (optional) String or List of Strings containing name
                           of or wildcards for content to archive. See <source>
                           Default is an Empty List (nothing)
            <exclusions> = (optional) String or List of Strings containing
                           name of or wildcards for content NOT to archive.
                           Default is an Empty List (nothing)
              <password> = (optional) Password to use to protect content. Only
                           available when 7zip is accessible!
                           Default is no password.
               <verbose> = (optional) Console display behavior.
                           Default is None (minimal) or value of global
                           verbose (see 'getVerboseHandles' function)
"""

    # Get verbose handles
    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    # Standardize variables
    if not password:
        password = ""
    if not isinstance( source, list):    # Allow for multiple sources
        source = [ "{0}".format( source)]
    if not inclusions:
        inclusions = []
    elif not isinstance( inclusions, list):	# Allow for multiple inclusions
        inclusions = [ "{0}".format( inclusions)]
    if not exclusions:
        exclusions = []
    elif not isinstance( exclusions, list):	# Allow for multiple exclusions
        exclusions = [ "{0}".format( exclusions)]

    if (os.access( zipFile, os.F_OK) and not os.access( zipFile, os.W_OK)) or not os.access( os.path.dirname( os.path.realpath( zipFile)), os.W_OK):
        raise Exception( "\n * Unable to write to archive '{0}' *".format( zipFile))
    else:
        # Check for 7Zip tool
        if utils.check7zip( verboseHandle=verboseCasual) == None:
            verboseDetail.write( "\n * Falling back to internal (slower) Python zip process! *\n")
            verboseCasual.write( " * 7Zip unavailable, using (slower) Python zip process!\n")

        # Check 7zip specific requirements
        if not utils.check7zip( verboseHandle=verboseCasual):
            # Alert user that password cannot be used without 7Zip
            if password:
                raise Exception( "\n * Unable to password protect archive without 7Zip! *")

            # Alert user that other archive types cannot be created without 7Zip
            if not zipFile.lower().endswith(".zip"):
                raise Exception( "\n * Unable to create this type of archive without 7Zip! *")

        matches = utils.OrderedDict()

        verboseCasual.write( "  Gathering file list...\n")

        # Search for source(s) and inclusion(s)
        for src in source + inclusions:
            # Set source to a real path name
            path = os.path.realpath( src)
            useRecursion = recurse

            if os.access( path, os.F_OK):
                baseLen = len( os.path.dirname( path)) + 1
                searchMask = "*"

                # Override Recursion if archiving a directory
                if os.path.isdir( path):
                    useRecursion = True
            else:
                path, searchMask = os.path.split( path)
                baseLen = len( path) + 1

                # Verify folder is accessible
                if not os.access( path, os.F_OK):
                    raise Exception( "\n * Unable to locate source content '{0}' *".format( source))

            # Get list of items needing archival
            for match in utils.iterPath( path, searchMask, exclusions=exclusions, recurse=useRecursion, verboseHandle=verboseCasual):
                # Store unique Path if absent
                baseIndex = match.find( os.sep, baseLen) + 1
                while baseIndex:
                    basePath = match[0:baseIndex]
                    if basePath not in matches:
                        matches[ basePath] = match[ baseLen:baseIndex]
                    baseIndex = match.find( os.sep, baseIndex) + 1

                if match not in matches:
                    # Store unique File by (key=value) pair using (Full=Abreviated) paths
                    matches[ match] = match[ baseLen:]

        outcome = None
        # Did we find anything to archive?
        if not matches:
            verboseCasual.write( " * Nothing found to archive! *\n")
        else:
            # If found, prep for 7Zip archive
            if utils.check7zip( verboseHandle=verboseCasual):
                callOptions = [
                    "7z",
                    "a",    # Add files
                    "-ssw", # Enable compress of shared files
                    "-y"    # Assume Yes on all questions
                ]

                # Add recursion
                if recurse:
                    callOptions.append( "-r")

                # Exclude compression
                if not useCompression:
                    callOptions.append( "-mx0")

                # Add password
                if password:
                    # Include 'maskPassword' text around password for display!
                    callOptions.append( "-p\*" + password + "\*")
                    password = True
                else:
                    password = False

                # Add inclusions
                for item in inclusions:
                    callOptions.append( "-i!" + item)

                # Add exclusions
                for item in exclusions:
                    callOptions.append( "-x!" + item)

                # Add output archive
                callOptions.append( zipFile)

                # Add specified content
                for src in source:
                    callOptions.append( src)

            else:	# Prep for Python archive

                # Set open mode - Overwrite by default
                zipMode = "w"
                if os.access( zipFile, os.F_OK):
                    if append:
                        zipMode = "a"
                        append = "Updating"
                    else:
                        append = "Overwriting"
                else:
                    append = "Creating"

                # Set compression
                if not useCompression:
                    zipCompression = zipfile.ZIP_STORED
                    useCompression = "Storing"
                else:
                    zipCompression = zipfile.ZIP_DEFLATED
                    useCompression = "Compressing"

            # Initiate Archive
            ZipFile = None

            try:
                verboseCasual.write( "  Archiving...")

                if utils.check7zip( verboseHandle=verboseCasual):
                    # Delete existing Zip file if not appending
                    if os.access( zipFile, os.F_OK) and not append:
                        os.remove( zipFile)

                    outcome = utils.callCommandLine( callOptions, verbose=(verbose == True), maskPassword=password)[0]
                else:
                    verboseDetail.write( "\nUsing Python zipfile object\n")
                    verboseDetail.write( "\n{0} archive {1}\n\n".format( append, zipFile))

                    # Open zip file
                    ZipFile = zipfile.ZipFile( zipFile, zipMode, zipCompression)

                    # Archive using list of matches
                    for item in matches.iterkeys():
                        if item.endswith( os.sep):
                            # Create ZipInfo object for Directory entry
                            DirInfo = zipfile.ZipInfo( matches[ item], time.localtime( os.path.getmtime( item))[0:6])
                            DirInfo.external_attr = 16
                            DirInfo.compress_type = zipfile.ZIP_STORED
                            ZipFile.writestr( DirInfo, "")
                        else:
                            verboseCasual.write( ".")
                            verboseDetail.write( "{0}  {1}\n".format( useCompression, matches[ item]))
                            ZipFile.write( item, matches[ item])

                    outcome = 0
                    verboseDetail.write( "\nEverything is Ok\n")

            except Exception as e:
                outcome = e

            if ZipFile:
                ZipFile.close()

            if outcome == 0:
                verboseCasual.write( "Success\n")
            else:
                verboseCasual.write( "Failed! Outcome: '{0}'\n". format( outcome))
                if ZipFile:
                    os.remove( zipFile)	# Remove the incomplete archive file

            return (outcome == 0)

#############################################
# Set File Last Modified/Access timestamp.  #
#                                           #
# Build: v1.0.0, Nov 2012, Paul Dodd - esri #
#############################################

def setFileTime( filename, timestamp=None):

    """Function: setFileTime( <filename>, [<timestamp>])

    Set a file's Last Modified and Last Accessed timestamps.

    Where:
         <filename> = Filename and optional Path to File that will be changed.
        <timestamp> = (optional) UTC Datetime object that will be used to set
                      date/time values.
                      Default is None. This will set file time to current time
                      essentially a unix 'touch' command.
"""
    if timestamp:
        # Calc Time Delta of file using Epoch, then compute UTC Total Seconds
        td = timestamp - datetime.datetime.utcfromtimestamp( 0)
        fileTime = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        timestamp = ( fileTime, fileTime)
    else:
        timestamp = None

    # Set file access and modified times
    os.utime( filename, timestamp)

################################################################
# Get Standard out and Standard err Handles for Verbose output #
#                                                              #
# Build: v1.0.0, Jan 2013, Paul Dodd - esri                    #
################################################################

def getVerboseHandles( verbose=None):
    """Function: getVerboseHandles( [<verbose>])

    Supplies console Verbose handles based on the specified or global verbose
    values.

    Returns:
        A two part Tuple containing File Handlers for Casual and Detailed
        feedback (in that order) depending on desired Verbose level. Like the
        sys.stdout (console) and sys.stderr (error out or current ALF log).

    Where:
        <verbose> = (optional) True, False, or None.
                     True: (show me everything) will return Console handler
                           for both Casual and Detailed feedback.
                    False: (don't show anything) will return current ALF log
                           if available or an open handle to the system's Null
                           device.
                     None: (the default) will return the Console handler and
                           either the current ALF log or the system's Null
                           device. * NOTE * If your import reference to
                           'ALFlib' includes an attribute called 'verbose',
                           this function will treat it as a global verbose
                           setting and override 'None' with the global value.

    Example Usage:

        import ALFlib

        # Set the default global Verbose for my routine
        ALFlib.verbose = False # I don't want to see anything on the console!

        def myFunction( message, verbose=None):
            verboseCasual, verboseDetail = ALFlib.getVerboseHandles( verbose)

            verboseCasual.write( 'Casual: ' + message)
            verboseDetail.write( 'Detail: ' + message)

        # Try with standard outputs
        myFunction( 'Hello World!\\n')
        print( 'Nothing should have printed...\\n')

        # Try with all console outputs
        myFunction( 'Hello World!\\n', True)
        print( 'Two should have printed...\\n')

        # Reset global verbose and try with standard outputs
        ALFlib.verbose = None
        myFunction( 'Hello World two!\\n')
        print( 'One should have printed...\\n')

        # Try with no output + ALFlog
        ALFlog = ALFlib.Logger( 'HelloWorld', '.')
        myFunction( 'Hello World two!\\n')
        print( 'One should have printed and three should be in the log...\\n')
"""
    if hasattr( utils, 'stderr'):
        # ALFlog in use?
        stderr = utils.stderr
    else:
        # Set global Null file
        if not hasattr( utils, 'DevNull'):
            utils.DevNull = open( os.devnull, 'w')
        stderr = utils.DevNull

    # Set global verbose
    if not hasattr( utils, 'verbose'):
        utils.verbose = None

    if verbose != False and (verbose or utils.verbose != False):
        # Local and Global Verbose are NOT False (requested off)
        if verbose or utils.verbose:
            # Local or Global Verbose is True (requested on), send all feedback to console
            return sys.stdout, sys.stdout
        else:
            # Local and Global Verbose are None (default), limit feedback
            return sys.stdout, stderr
    else:
        # Local or Global Verbose is False (requested off), send all feedback to log or Null
        return stderr, stderr

########################################################
# Call Command Line and return results                 #
#                                                      #
# Build: v1.1.0, Apr 2013, Paul Dodd - esri            #
#      - Added 'maskPassword' option to allow display  #
#        or logging of full command line that may also #
#        include a user password.                      #
# Build: v1.0.0, Jan 2013, Paul Dodd - esri            #
########################################################

def callCommandLine( callParams, description=None, timeout=0, timerHook=None, verbose=None, maskPassword=False):
    """Function: callCommandLine( <callParams>[, <description>[, <timeout>[, <timerHook>[, <verbose>]]]])

    Issue a Command Line call to run a process, returning its console output.
    Console output is automatically logged/displayed using verbose option.

    Returns:
        A two part Tuple containing an Integer Error Outcome and a List of
        strings that contain console output (in that order). An Exception is
        raised if an error condition is encountered. A TimeoutError Exception
        is raised when the process runs longer than <timeout> without console
        activity or a True response from <timerHook>.

    Where:
         <callParams> = String or List containing command line parameters to
                        execute. If String, parameters are parsed using a space
                        as a separator.
        <description> = (optional) Display string that describes the process.
                        Default is <callParams>, but not echoed to console.
            <timeout> = (optional) Interval in seconds before TimeoutError is
                        issued. A boolean (True or False) result from <timerHook>
                        can be used to influence timeout trigger.
                        Default is 0 (no timeout)
          <timerHook> = (optional) Function name to call during the process
                        'timeout' monitor loop (once every 0.25 seconds). As a
                        parameter, 'function' will receive the 'subprocess.Popen'
                        process object that was created to execute the command.
                        Use this feature to report progress or perform a specific
                        action as the process call runs. Return a boolean (True
                        or False) to influence the timeout cycle. True will reset
                        the timeout trigger back to <timeout> and False will
                        cancel the console activity detection (creating an
                        absolute timeout condition).
                        Default is None
            <verbose> = (optional) Console display behavior.
                        Default is None (minimal) or value of global
                        verbose (see 'getVerboseHandles' function)
       <maskPassword> = (optional) Visually mask password that may be included in
                        <callParams>. Used for logging command line before making
                        call. To indicate what should be masked, surround password
                        with '*' text. This option will remove the '*' text prior
                        to making call, and will only be identified in pairs! Single
                        or odd instances of this text is ignored. The mask is always
                        eight '*' characters regardless of the 'password' length.

                          Entered as: 'RunThis.exe -p *MyPassword* -o abc*123'
                        Displayed as: 'RunThis.exe -p ******** -o abc*123'
                         Executed as: 'RunThis.exe -p MyPassword -o abc*123'

                        True will enable option and False will disable it.
                        Default is False

    Example Usage:

        import ALFlib

        callOptions = [ 'ping', '-n', '5', 'esri.com']
        # or
        # callOptions = 'ping -n 5 esri.com'

        desc = 'Checking for reply from Esri...'

        outcome, response = ALFlib.callCommandLine( callOptions, descripiton=desc, verbose=True)

        # Show Timeout Hook
        def hookFunction( process):
            print( '.') # Dot progress every 1/4 second

        ALFlib.callCommandLine( callOptions, verbose=True, timerHook=hookFunction)
"""
    # Setup Verbose Object
    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    outcome = 0
    results = []
    ErrorException = None

    if not callParams:
        verboseDetail.write( "\ncallCommandLine: * No call parameters provided *\n")
    else:
        # Structure call parameters
        if not isinstance( callParams, list):
            # String or unicode?
            if hasattr( callParams, 'split'):
                callParams = callParams.split()
            else:
                callParams = ['{0}'.format( callParams)]

        # Mask Password for display
        if maskPassword:
            command = ''
            sep = ''

            # Parse each call parameter
            for index in range( len( callParams)):
                tail = '{0}'.format( callParams[ index])
                exposedOption = ''
                maskedOption = ''

                while tail:
                    parts = tail.split( '\*', 2)
                    if len( parts) > 2:
                        exposedOption += parts[0] + parts[1]
                        maskedOption += parts[0] + '********'
                        tail = parts[2]
                    else:
                        exposedOption += tail
                        maskedOption += tail
                        tail = ''

                if exposedOption:
                    callParams[ index] = exposedOption

                command += sep + maskedOption
                sep = ' '
        else:
            command = ' '.join( callParams)

        # Report details
        if description:
            verboseCasual.write( "\ncallCommandLine: \"{0}\"\n".format( description))
            verboseDetail.write( "call Parameters: \"{0}\"\n".format( command))
        else:
            verboseDetail.write( "\ncallCommandLine: \"{0}\"\n".format( command))

        # Setup timer details
        cycleTime = float( 250)	# in Milliseconds
        sleepTime = cycleTime / 1000	# in Fractions of a second

        with tempfile.TemporaryFile() as logFP:
            verboseDetail.write( "Console Feedback:\n-------------\n")
            logFN = logFP.fileno()
            seekIndex = 0
            resetCycle = True
            startTime = datetime.datetime.now()

            try:
                process = subprocess.Popen( callParams, stdout=logFN, stderr=logFN)

                lastSize = 0
                while process.poll() == None:
                    # Setup/reset timeout cycle
                    if resetCycle:
                        resetCycle = False
                        if timeout and (type( timeout) == int) and sleepTime:
                            cycles = timeout / sleepTime
                        else:
                            cycles = -1	# Infinite wait, but still monitor process

                    # Check timeout
                    if not cycles:
                        process.kill()
                        raise utils.TimeoutError( "Exceeded {0} second timeout while waiting for command line process to return!".format( timeout))

                    cycles -= 1

                    # Check for Log activity
                    try:
                        logFP.flush()            # Flush the buffer
                    except:
                        pass
                    currentSize = os.fstat( logFN).st_size	# Get the current size
                    if (currentSize - lastSize):        # Any change?
                        lastSize = currentSize
                        resetCycle = True        	# Trigger Cycle Reset

                        # Record/report output
                        logFP.seek( seekIndex)
                        for buffer in logFP.readlines():
                            if (seekIndex + len(buffer)) < currentSize:	# Read all but last line
                                seekIndex += len(buffer)
                                buffer = buffer.rstrip()
                                verboseDetail.write( buffer + "\n")
                                results.append( buffer)

                    # Call user function
                    if timerHook and callable( timerHook):
                        hookOutcome = timerHook( process)	# Call and Set re-cycle flag on return
                        if isinstance( hookOutcome, bool):
                            resetCycle = hookOutcome

                    time.sleep( sleepTime)

                outcome = process.returncode

            except EnvironmentError as e:
                outcome = e.errno
                results.append( e.strerror)
                verboseDetail.write( e.strerror + "\n")
                ErrorException = e

            except Exception as e:
                ErrorException = e

            # Invoke timerHook one last time to allow any final user processing logic
            if timerHook and callable( timerHook):
                timerHook( process)

            # Record/report final output, if any
            logFP.seek( seekIndex)
            for buffer in logFP.readlines():
                buffer = buffer.rstrip()
                verboseDetail.write( buffer + "\n")
                results.append( buffer)

            if not results:
                verboseDetail.write( " * No console feedback was detected *\n")

            verboseDetail.write( "-------------\nCall Outcome: {0}, Elapsed Time: {1}\n\n".format( outcome, utils._formatTimeDelta( datetime.datetime.now() - startTime, stripStr="")))

    if ErrorException:
        raise ErrorException

    return outcome, results

#############################################
# Recursive File Search function            #
#                                           #
# Build: v2.0.0, Apr 2015, Paul Dodd - esri #
#      - Now leverages the 'iterPath' func. #
# Build: v1.1.0, Feb 2014, Paul Dodd - esri #
#      - Added 'caseSensitive' option       #
# Build: v1.0.0, Jan 2013, Paul Dodd - esri #
#############################################

def recursePath( path, mask, exclusions=None, matches=None, recurse=True, verboseHandle=None, caseSensitive=True):
    """Function: recursePath( <path>, <mask>[, <exclusions>[, <matches>[, <recurse>[, <verboseHandle>[, <caseSensitive>]]]]])

    Mainly used by internal routines that perform recursive directory searches.
    Can be leveraged to search for files that meet a given criteria.

    Returns:
        A List of Strings containing the names of the files (with complete paths)
        that match the target details.

    Where:
                 <path> = String folder path and/or name of file to search.
                 <mask> = String containing file system wildcard that should be
                          used to match files or folders. Like '*' or 'abc??.d*'
           <exclusions> = (optional) String or List of Strings containing
                          name of or wildcards for content NOT to match.
                          Default is an Empty List (nothing)
              <matches> = (optional) List containing Strings of files that match
                          so far (used by function to quickly append its findings)
                          Default is an Empty List (nothing)
              <recurse> = (optional) True or False. Specify whether or not
                          to recursively search a directory's contents.
                          Default is True
        <verboseHandle> = (optional) File handle of where to send warnings.
                          Default is 'sys.stderr'. (see 'getVerboseHandles')
        <caseSensitive> = (optional) Specify if search should be case sensitive.
                          Default is True
"""

    # Standardize variables
    if not matches or not isinstance( matches, list):
        matches = []        # Ensure that 'matches' is an empty list!

    for match in utils.iterPath( path, mask, exclusions=exclusions, recurse=recurse, verboseHandle=verboseHandle, caseSensitive=caseSensitive):
        matches.append( match)

    return matches

#############################################
# Iterate File Search function              #
#                                           #
# Build: v1.0.0, Jan 2013, Paul Dodd - esri #
#############################################

def iterPath( path, mask, exclusions=None, recurse=True, verboseHandle=None, caseSensitive=True):
    """Function: iterPath( <path>, <mask>[, <exclusions>[, <recurse>[, <verboseHandle>[, <caseSensitive>]]]])

    Mainly used by internal routines that perform recursive directory searches.
    Can be leveraged to search for files that meet a given criteria.

    Returns:
        An Iterable Generator object of Strings containing the names of the files
        (with complete paths) that match the target details.

    Where:
                 <path> = String folder path and/or name of file to search.
                 <mask> = String containing file system wildcard that should be
                          used to match files or folders. Like '*' or 'abc??.d*'
           <exclusions> = (optional) String or List of Strings containing
                          name of or wildcards for content NOT to match.
                          Default is an Empty List (nothing)
              <recurse> = (optional) True or False. Specify whether or not
                          to recursively search a directory's contents.
                          Default is True
        <verboseHandle> = (optional) File handle of where to send warnings.
                          Default is 'sys.stderr'. (see 'getVerboseHandles')
        <caseSensitive> = (optional) Specify if search should be case sensitive.
                          Default is True
"""

    # Standardize variables
    if not isinstance( verboseHandle, file):
        verboseHandle = sys.stderr    # Default to Standard Error
    if not exclusions:
        exclusions = []
    elif not isinstance( exclusions, list):	# Allow for single or multiple string exclusions
        exclusions = [ "{0}".format( exclusions)]

    fnFunc = fnmatch.fnmatch
    if caseSensitive:
        fnFunc = fnmatch.fnmatchcase

    def __iter__( path=None):
        try:
            # Check if path is a file
            if os.path.isfile( path):
                for exclusion in exclusions:
                    if fnFunc( path, exclusion):
                        break
                else:
                    if fnFunc( path, mask):
                        yield path
            else:
                for item in os.listdir( path):
                    lastPath = os.path.join( path, item)
                    folder = " Folder" if os.path.isdir( lastPath) else ""
                    try:
                        for exclusion in exclusions:
                            if fnFunc( lastPath, exclusion):
                                verboseHandle.write( " * Excluding{0}: '{1}', for Exclusion: '{2}'\n".format( folder, lastPath, exclusion))
                                break
                        else:
                            if folder:
                                if recurse:
                                    for item in __iter__( lastPath):
                                        yield item

                            elif os.path.isfile( lastPath):
                                if fnFunc( item, mask):
                                    yield lastPath

                    except EnvironmentError as e:
                        verboseHandle.write( " * Skipping: '{0}', for Reason: {1}\n".format( e.filename, e.args[1]))

        finally:
            pass

    return __iter__( path)

#############################################
# Copy Files from one location to another   #
#                                           #
# Build: v1.0.1, Apr 2013, Paul Dodd - esri #
#     - Updated copy failure to report file #
#       copy issue, but not throw an        #
#       Exception until completion.         #
# Build: v1.0.0, Jan 2013, Paul Dodd - esri #
#############################################

def copyFiles( source, destination=".", exclusions=[], overwrite=False, recurse=False, showProgress=True, verbose=None):
    """Function: copyFiles( <source>[, <destination>[, <exclusions>[, <overwrite>[, <recurse>[, <showProgress>[, <verbose>]]]]]])

    Copies one or more files from one location to another. If source is a
    folder, the routine will recursively copy all files in all folders (as
    long as the file is not excluded by <exclusions> list).

    Returns:
        Number of files copied. Or raises exception for a serious issue.

    Where:
              <source> = String containing path and/or name of content to
                         copy. Can include file system compatible wildcards.
                         If <source> is a folder, all contents (including
                         the folder, minus exclusions) are copied and
                         <recurse> setting is ignored.
         <destination> = (optional) String containing location of where to
                         copy contents to. (path is created if not exist)
                         Default is current directory
          <exclusions> = (optional) String or List of Strings containing
                         name of or wildcards for content NOT to match.
                         Default is an Empty List (nothing)
           <overwrite> = (optional) True or False. Specify whether or not
                         to forcibly write over content that already exists,
                         regardless of age or size.
                         Default is False
             <recurse> = (optional) True or False. Specify whether or not
                         to recursively copy a directory's contents.
                         Default is False (ignored if <source> is a folder)
        <showProgress> = (optional) True or False. Specify whether or not
                         display progress % to console, ignoring verbose.
                         Default is True
             <verbose> = (optional) Console display behavior.
                         Default is None (minimal) or value of global
                         verbose (see 'getVerboseHandles' function)
"""

    # Set source and destination to real paths
    src = os.path.realpath( source)
    dest = os.path.realpath( destination)

    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    if showProgress:
        Progress = utils.Progress()

    if os.access( src, os.F_OK):
        baseLen = len( os.path.dirname( src)) + 1
        searchMask = "*"

        # Override Recursion if source is a directory
        if os.path.isdir( src):
            recurse = True
    else:
        src, searchMask = os.path.split( src)
        baseLen = len( src) + 1

        # Verify source is accessible
        if not os.access( src, os.F_OK):
            raise Exception( "Unable to locate source content '{0}'!".format( source))

    # Verify destination
    if os.access( dest, os.F_OK):
        if not os.path.isdir( dest):
            raise Exception( "Copy destination is not a folder: '{0}'".format( destination))
    else:
        try:
            os.makedirs( dest)
        except Exception as e:
            raise Exception( "Unable to create destination '{0}': {1}".format( destination, e))

    # Verify source and destination are different
    #if src.startswith( dest + os.sep):
    if src[0:baseLen-1] == dest:
        raise Exception( "Source cannot equal Destination!")

    verboseCasual.write( "  Gathering file list...\n")

    # Get list of items needing to be copied
    matches= utils.recursePath( src, searchMask, exclusions=exclusions, recurse=recurse, verboseHandle=verboseCasual)

    if not matches:
        verboseCasual.write( "\n * Nothing found to copy *\n")
        return 0
    else:
        verboseCasual.write( "\n  Copying From:\n    '{0}'\n  to:\n    '{1}'...\n\n".format( src, dest))

        fileStats = { 'copied': 0, 'overwritten': 0, 'skipped': 0, 'failed': 0}
        totalFiles = len( matches)
        filesCopied = 0
        startTime = datetime.datetime.now()

        for input in matches:
            try:
                file = input[baseLen:]
                output = os.path.join( dest, file)

                if showProgress and Progress.willDisplay():
                    percent = float( filesCopied) / totalFiles
                    Progress.display( "{0: 6.0%} complete...".format( percent))

                # Does output file exist?
                if os.access( output, os.F_OK):
                    if not overwrite:
                        destModified = datetime.datetime.utcfromtimestamp( os.stat( output).st_mtime)
                        destModified -= datetime.timedelta( microseconds=destModified.microsecond)
                        srcModified = datetime.datetime.utcfromtimestamp( os.stat( input).st_mtime)
                        srcModified -= datetime.timedelta( microseconds=srcModified.microsecond)
                        if destModified > srcModified:
                            raise Warning( "Destination is newer")
                        if destModified == srcModified:
                            if os.stat( output).st_size == os.stat( input).st_size:
                                raise Warning( "Destination matches source")
                        statText = "Updating"
                    else:
                        statText = "Overwriting"
                    statIndex = 'overwritten'
                else:
                    statIndex = 'copied'
                    statText = "Copying"

                    # Create missing output directories
                    if not os.access( os.path.dirname( output), os.F_OK):
                        srcDir = input[0:baseLen]
                        destDir = dest
                        for subDir in os.path.dirname( file).split( os.sep):
                            srcDir = os.path.join( srcDir, subDir)
                            destDir = os.path.join( destDir, subDir)
                            if not os.access( destDir, os.F_OK):
                                verboseDetail.write( "    Creating Directory: '{0}'\n".format( destDir))
                                os.mkdir( destDir)    	# Create Directory
                                try:
                                    shutil.copystat( srcDir, destDir)	# Copy permissions
                                except Exception as e:
                                    verboseDetail.write( "  * Unable to set directory permissions on '{0}': {1}".format( destDir, e))

                verboseDetail.write( "    {0}: '{1}'\n".format( statText, file))

                # Copy file
                shutil.copy2( input, output)

                # Update stats
                fileStats[ statIndex] += 1
                filesCopied += 1

            except Warning as w:
                fileStats[ 'skipped'] += 1
                verboseDetail.write( "  * Skipping - {0}: '{1}'\n".format( w, input))
            except Exception as e:
                fileStats[ 'failed'] += 1
                verboseDetail.write( "  * Unable to copy file '{0}': {1}\n".format( input, e))
        else:
            verboseDetail.write( "\n")	# Add newline to log
            if showProgress:
                if fileStats[ 'failed']:
                    Progress.clear( "  Copy completed, with failures!")
                else:
                    Progress.clear( "  Copy completed!")

        verboseCasual.write( "\n       Files Copied: {0: 3d}\n".format( fileStats[ 'copied']))
        verboseCasual.write( "  Files Overwritten: {0: 3d}\n".format( fileStats[ 'overwritten']))
        verboseCasual.write( "      Files Skipped: {0: 3d}\n".format( fileStats[ 'skipped']))
        verboseCasual.write( "      Copy failures: {0: 3d}\n".format( fileStats[ 'failed']))

        verboseDetail.write( "\n  Elapsed Time for Copy: {0}\n".format( utils._formatTimeDelta( datetime.datetime.now() - startTime, stripStr="")))

        if fileStats[ 'failed']:
            if fileStats[ 'failed'] == 1:
                raise Exception( "Failed to copy 1 file!")
            else:
                raise Exception( "Failed to copy {0} files!".format( fileStats[ 'failed']))

        return fileStats[ 'copied'] + fileStats[ 'overwritten']

#############################################
# Retry execution of a Function or Method   #
#                                           #
# Build: v1.1.0, Sep 2014, Paul Dodd - esri #
#      - Added Keyword Argument support     #
# Build: v1.0.0, Dec 2013, Paul Dodd - esri #
#############################################

def retryIt( function, args=(), attempts=3, pause=2, retryHook=None, kwargs={}):
    """Function: retryIt( <function>[, <args>[, <attempts>[, <pause>]]])

    Executes a given function or method, passing in arguments. If <function>
    throws an Exception, retryIt will <pause> a given number of seconds before
    the <function> will be retried again. This process continues until the call
    is successful or until <attempts> count has elapsed.

    Returns:
        Results of <function> or final Exception is thrown if <attemps> expire.

    Where:
         <function> = Function or Method to call.

             <args> = (optional) Argument list to pass to <function>. Depends on
                      requirements of <function>. Can be used with <kwargs>.
                      Default is empty list
         <attempts> = (optional) Number of call attempts to make to <function>.
                      Default is 3
            <pause> = (optional) Seconds to pause between call attampts.
                      Default is 2
        <retryHook> = (optional) Function or Method to call during retry logic.
                      This call is performed prior to <pause> and before the
                      next attempt to call <function>. If <retryHook> supports
                      arguments, then the Error Exception will be included in
                      call to <retryHook> function. If call to <retryHook>
                      returns and non-empty result, additional retry attempts
                      will be canceled!
                      Default is None
           <kwargs> = (optional) Dictionary containing Keyword Arguments and
                      values for <function>. Can be used with <args>.

    Example Usage:

        import ALFlib

        ALFlib.retryIt( ALFlib.getDownload, ["www.noaa.gov/data/filename.txt"])
        or
        ALFlib.retryIt( <someObject>.<someMethod>, [<arg>, <arg>, ...], pause=1)
        or
        ALFlib.retryIt( <someObject>.<someMethod>, kwargs={"<arg>": <value>, "<arg>": <value>, ...}, pause=1)
"""
    if callable( function):
        count = 0
        functionName = "{0}.{1}".format( function.__module__, function.__name__)

        if not (isinstance( args, list) or isinstance( args, tuple)):
            args = [args]

        if kwargs and not isinstance( kwargs, dict):
            raise Exception( "Expecting Keyword Arguments as Dictionary")

        while True:
            count += 1
            try:
                if args:
                    if kwargs:
                        return function( *args, **kwargs)
                    else:
                        return function( *args)
                elif kwargs:
                    return function( **kwargs)
                else:
                    return function()

            except Exception as e:
                sys.stderr.write( "\n * Failed to call function '{0}'...\n".format( functionName))

                cancel = False
                if retryHook and callable( retryHook):
                    try:
                        if inspect.getargspec( retryHook)[0]:
                            # If args supported, pass in exception details
                            cancel = retryHook( e)
                        else:
                            cancel = retryHook()
                    except Exception as eHook:
                        sys.stderr.write( "\n * retryIt: Unable to call retryHook '{0}', ignored because of: '{1}'\n".format( retryHook.__name__, eHook))

                sys.stderr.write( "\n * Encountered exception: '{0}'\n".format( str(e).strip()))

                if attempts - count <= 0:
                    if count > 1:
                        sys.stderr.write( "\n * Retry limit exhausted *\n")
                    raise

                if cancel:
                    if isinstance( cancel, bool):
                        sys.stdout.write( "\n * Retry was Canceled *\n")
                    else:
                        sys.stdout.write( "\n * Retry was Canceled, detected: '{0}' *\n".format( cancel))
                    raise

                sys.stdout.write( "\n * Try {0} of {1} *\n".format( count+1, attempts))
                time.sleep( pause)
    else:
        raise Exception( "Function '{0}' is not callable, cannot invoke retry".format( function))

######################
# semdEmail fucntion #
######################

def sendEmail( fromAddr="", toAddr=(), subject="", body="", ccAddr=(), bccAddr=(), attachments=(), importance="normal" or "low" or "high", sensitivity="", server="", port=(), userName="", password="", useSSL=None, keyFile=None, certFile=None, timeout=0, verbose=None, subType="plain", tries=0, delay=0, details=False):
    """Function: sendEmail( [<fromAddr>[, <toAddr>[, <subject>[, <body>[, <ccAddr>[, <bccAddr>[, <attachments>[, <importance>[, <sensitivity>[, <server>[, <port>[, <userName>[, <password>[, <verbose>[, <useSSL>[, <keyFile>[, <certFile>[, <timeout>[, <subType>[, <tries>[, <delay>[, <details>]]]]]]]]]]]]]]]]]]]]]])

    Send E-Mail and attachments to recipients using secured or unsecured SMTP
    Mail Protocol.

    Returns:
        True on success.
        Raises Exception on failure or when no e-mail recipients are supplied.

        If <details> is True and send is successful, a Dictionary like the
        following will be returned, reflecting the outcome:
            { "attempt": 2, "server": "MyEmailServer.domain.com"}

    Where:
           <fromAddr> = (optional) E-mail address of sender in the form of
                        <user>@<domain>. <user> is optional, local machine name
                        will be used if not supplied. <domain> is optional,
                        <server> domain will be used if not supplied.
                        Supports e-mail Alias when address includes '<>' chars.
                        Ex. 'ALF Routine <pdodd@esri.com>' using full address
                            'ALF Routine <@esri.com>' using domain w/o user
                            'ALF Routine <pdodd>' using e-mail user w/o domain
                            'ALF Routine <>' using no e-mail address
                        Default to Environment Variable: 'ALFmail_From'
                        Falling back to local machine name @ local domain, in
                        addition, the e-mail's 'Reply-To' address will be set
                        to 'NoReply@<domain>'
             <toAddr> = (optional, but required if no <ccAddr> or <bccAddr>
                        value supplied) A comma or semi-colon separated String
                        or Iterable containing recipient e-mail addresses.
                        Default to Environment Variable: 'ALFmail_To'
                        Falling back to None
            <subject> = (optional) String containing e-mail subject line text.
                        Default is None
               <body> = (optional) String containing text of e-mail body.
                        Default is None
             <ccAddr> = (optional, but required if no <toAddr> or <bccAddr>
                        value supplied) A comma or semi-colon separated String
                        or Iterable containing recipient e-mail addresses to
                        Carbon Copy to.
                        Default to Environment Variable: 'ALFmail_CC'
                        Falling back to None
            <bccAddr> = (optional, but required if no <toAddr> or <ccAddr>
                        value supplied) A comma or semi-colon separated String
                        or Iterable containing recipient e-mail addresses to
                        Blind Carbon Copy to.
                        Default to Environment Variable: 'ALFmail_BCC'
                        Falling back to None
        <attachments> = (optional) String or Iterable containing String file
                        paths of content to include as attachments to e-mail.
                        Default is None
         <importance> = (optional) Flag e-mail importance using String or
                        partial unique String of characters from: 'N[ormal]',
                        'L[ow]', or 'H[igh]'
                        Default is Normal importance
        <sensitivity> = (optional) Flag e-mail sensitivity using String or
                        partial unique String of characters from: 'N[ormal]',
                        'Pe[rsonal]', 'Pr[ivate]', or 'C[ompany-Confidential]
                        or simply C[onfidential]'
                        Default to Environment Variable: 'ALFmail_Sensitivity'
                        Falling back to Normal sensitivity
             <server> = (optional) A comma or semi-colon separated String or
                        Iterable containing name or IP address list of valid
                        SMTP mailservers to use.
                        * NOTE * ALL Servers MUST use the same domain!!
                        To enable LMTP for Unix socket path connection, ensure
                        server's socket path begins with '/'.
                        Default to Environment Variable: 'ALFmail_Server'
                        Falls back to automatic search for most preferred MX
                        server. Local domain is searched when <fromAddr> domain
                        is local.
                        Otherwise the specified <fromAddr> domain is used.
               <port> = (optional) Integer TCP port number to use for transport.
                        Default to Environment Variable: 'ALFmail_Port'
                        Falls back to 25 for unsecured and 465 for secured (SSL)
           <userName> = (optional) Mail server user account.
                        Default to Environment Variable: 'ALFmail_Username'
                        Falling back to <fromAddr> less domain, and only used
                        with <password>.
           <password> = (optional) Mail server user account password.
                        Default to Environment Variable: 'ALFmail_Password'
                        Falling back to None
             <useSSL> = (optional) Use secured SSL connection to mail server
                        when True.
                        Default to Environment Variable: 'ALFmail_SSL'
                        Falling back to False, use unsecured connection
            <keyFile> = (optional) String path to PEM formatted private key
                        file passed to SSL connection.
                        Default to Environment Variable: 'ALFmail_Key'
                        Falling back to None. Ignored when not using SSL
           <certFile> = (optional) String path to PEM formatted certificate
                        chain file passed to SSL connection.
                        Default to Environment Variable: 'ALFmail_Certificate'
                        Falling back to None. Ignored when not using SSL
            <timeout> = (optional) Connection timeout in integer seconds.
                        Default to Environment Variable: 'ALFmail_Timeout'
                        Falling back to 30
            <verbose> = (optional) Console display behavior.
                        Default is None (minimal) or value of global
                        verbose (see 'getVerboseHandles' function)
            <subType> = (optional) Content format sub-type for body text. Can
                        be 'plain', 'html', 'enriched', 'rtf', or other.
                        For more details and options, see:
                        'https://en.wikipedia.org/wiki/Formatted_text'
                        Default is 'plain'
              <tries> = (optional) Number of connection attempts that should be
                        allowed before giving up.
                        Default to Environment Variable: 'ALFmail_Tries' or 3
                        Minimum is 1
              <delay> = (optional) Number of seconds to wait between connection
                        attempts.
                        Default to Environment Variable: 'ALFmail_Delay' or 5
            <details> = (optional) When set to True, returns Dictionary of
                        details on send success. When set to False, returns
                        original (pre v2.2) boolean True on send success.
                        Default to False (pre v2.2 behavior)

    Example Usage:

        import ALFlib

        ALFlib.sendEmail( toAddr="bobhope@hollywood.com", subject="Latest award", body="Hey Bob,\\nCongrats on your latest award!\\nWarm regards, Leslie")
        or
        ALFlib.sendEmail( fromAddr="me@myDomain.com", bccAddr=["you@yourDomain.com", "dupree@hisDomain.com"], importance="hi", sensitivity="Company")
        or
        ALFlib.sendEmail( toAddr="me@esri.com", subject="Test", body="<color><param>red</param>Blood</color> is <bold>thicker</bold> than <color><param>blue</param>water</color>.", subType="enriched")
"""

    import smtplib
    import email.mime.application
    import email.mime.audio
    import email.mime.image
    import email.mime.multipart
    import email.mime.text

    verboseCasual, verboseDetail = utils.getVerboseHandles( verbose)

    # Set default values to ALFmail Environment variables if available!
    fromAddr = fromAddr if fromAddr else os.environ.get( "ALFmail_From", "")
    toAddr = toAddr if toAddr else os.environ.get( "ALFmail_To", ())
    ccAddr = ccAddr if ccAddr else os.environ.get( "ALFmail_CC", ())
    bccAddr = bccAddr if bccAddr else os.environ.get( "ALFmail_BCC", ())
    sensitivity = sensitivity if sensitivity else os.environ.get( "ALFmail_Sensitivity", "normal" or "personal" or "private" or "company-confidential")
    server = server if server else os.environ.get( "ALFmail_Server", "")
    port = port if port else os.environ.get( "ALFmail_Port", ())
    userName = userName if userName else os.environ.get( "ALFmail_Username", "")
    password = password if password else os.environ.get( "ALFmail_Password", "")
    useSSL = useSSL if isinstance( useSSL, bool) else getEnviron( "ALFmail_SSL", bool, False)
    keyFile = keyFile if keyFile else os.environ.get( "ALFmail_Key", None)
    certFile = certFile if certFile else os.environ.get( "ALFmail_Certificate", None)
    timeout = timeout if timeout else getEnviron( "ALFmail_Timeout", int, 30)
    tries = tries if tries else getEnviron( "ALFmail_Tries", int, 3)
    delay = delay if delay else getEnviron( "ALFmail_Delay", int, 5)

    if not (toAddr or ccAddr or bccAddr):
        raise Exception( "sendEmail requires at least one Recipient")

    # Handle Server as iterable
    servers = []
    if server:
        if isinstance( server, basestring):
            for chr in ",;":
                if chr in server:
                    servers = server.split( chr)
                    server = servers[0]
                    break
            else:
                servers = [server]
        else:
            for item in server:
                servers.append( item)
            server = servers[0]

    def findMailServer( domain, servers=[]):
        # Enlist 'nslookup' to identify MX mail servers, then test
        outcome, reply = utils.callCommandLine( ["nslookup", "-type=MX", domain], verbose=verbose)

        if outcome:
            raise Exception( " - 'sendEmail' Find Mail Server failed with outcome: {0}, reply: '{1}'".format( outcome, reply))

        for line in reply:
            if "mail exchanger" in line:
                # Add by [preference, name]
                if "," in line:
                    # Windows result
                    servers.append( [line.split(",", 1)[0].split()[-1], line.split()[-1]])
                else:
                    # Unix result
                    servers.append( [line.split()[-2], line.split()[-1].strip(".")])

        if servers:
            # Sort list by preference from Highest (0) to Lowest (100)
            servers.sort()

        count = 0
        for preference, server in servers:
            count += 1
            try:
                socket.create_connection( (server, port), timeout=3).close()
                smtp.connect( server, port)
                return server

            except Exception as e:
                if not preference == "-1":  # Ignore if server is localhost default
                    verboseDetail.write( " * 'sendEmail' Server connection {0} of {1} failed. Server: '{2}', Error: '{3}'\n".format( count, len( servers), server, e))
                continue # try the next MX server in list

    def createAttachment( filename):
        import imghdr, sndhdr

        if imghdr.what( filename):
            mimeType = email.mime.image.MIMEImage
        elif sndhdr.what( filename):
            mimeType = email.mime.audio.MIMEAudio
        else:
            mimeType = email.mime.application.MIMEApplication

        # Create attachment message from file
        with open( filename, "rb") as iFP:
            mime = mimeType( iFP.read())
            mime.add_header('Content-Disposition', 'attachment', filename=os.path.split( filename)[-1])
            return mime

    # Setup SMTP object to use
    if useSSL:
        defaultPort = 465
        smtp = smtplib.SMTP_SSL( keyfile=keyFile, certfile=certFile, timeout=timeout)
        if not port:
            port = defaultPort
    else:
        defaultPort = 25
        if server and isinstance( server, basestring) and server.startswith( "/"):
            # Use Unix Socket connection
            verboseCasual.write( " - 'sendEmail' using socket connection\n")
            smtp = smtplib.LMTP()
        else:
            smtp = smtplib.SMTP( timeout=timeout)

        if not port:
            port = defaultPort

    try:
        if verbose or (verbose is None and utils.verbose):
            # Turn on debugging detail
            smtp.set_debuglevel( 1)

        # Setup initial Mail Message
        if attachments:
            msg = email.mime.multipart.MIMEMultipart()

            if isinstance( attachments, basestring) or not "__len__" in dir( attachments): # Is a String or not iterable, make it iterable!
                attachments = [attachments]

            for attachment in attachments:
                try:
                    msg.attach( createAttachment( attachment))
                except Exception as e:
                    verboseCasual.write( " * 'sendEmail' Attachment: error accessing '{0}', ignored!\n   Error: '{1}'\n".format( attachment, e))
                    body += "\n * Failed to add attachment: '{0}', '{1}' *".format( attachment, e)

            msg.attach( email.mime.text.MIMEText( body, _subtype=subType, _charset="UTF-8"))
        else:
            msg = email.mime.text.MIMEText( body, _subtype=subType, _charset="UTF-8")

        # Setup Port number
        verboseCasual.write( " - 'sendEmail' Port: ")
        if isinstance( port, int) and port >= 0 and port <= 65535:
            verboseCasual.write( "{0}\n".format( port))
        else:
            port = defaultPort
            verboseCasual.write( "invalid. Defaulting to {0}!\n".format( port))

        # Get Local Hostname and Domain
        fqdn = socket.getfqdn()
        hostname = fqdn.split( ".", 1)[0]
        domain = fqdn.split( ".", 1)[-1]
        fromDomain = ""
        connected = False
        noReplyTo = False

        # Check for Domain
        if domain == hostname:
            verboseDetail.write( "\n - No Host Domain available, initiating look-up...\n")
            domain = utils.getNetworkDetails( verbose=verbose).get( "localDomain", None)
            if domain:
                fqdn = ".".join( [ hostname, domain])
            else:
                domain = hostname

        # Setup Sender Alias String
        aliasString = "{0}@{1}"
        if "<" in fromAddr and ">" in fromAddr:
            alias, fromAddr = fromAddr.split( "<")
            fromAddr = fromAddr.split( ">")[0]
            aliasString = "{0} <{1}>".format( alias.strip(), aliasString)

        # Extract initial Sender details
        if "@" in fromAddr:
            fromAddr, fromDomain = fromAddr.split( "@", 1)

        if not fromAddr:
            fromAddr = hostname.capitalize()
            noReplyTo = True
            if not (fromDomain or domain == hostname):
                fromDomain = domain

        # Setup Mail Server
        verboseCasual.write( " - 'sendEmail' Server(s): ")
        if server:
            verboseCasual.write( "specified as {0}\n".format( servers))
            domain = server.split(".", 1)[-1]
        else:
            if hasattr( utils, "emailServer"):
                server = utils.emailServer
                domain = utils.emailDomain
                servers = [server]
                if not fromDomain or (domain == fromDomain):
                    verboseCasual.write( "re-using last discovered '{0}'\n".format( server))
                else:
                    # Force a Re-discover!
                    server = ""

            if not server:
                if fromDomain and (not fromDomain == domain):
                    # Get domain from sender
                    domain = fromDomain
                    verboseCasual.write( "Checking Sender Domain '{0}'\n".format( domain))
                else:
                    verboseCasual.write( "Checking Local Domain '{0}'\n".format( domain))

                # Check for available Mail Servers, include localhost as a default
                server = findMailServer( domain, servers=[["-1", "localhost"]])
                if server:
                    verboseCasual.write( "   Found Mail Server: '{0}'\n".format( server))
                    connected = True
                    domain = server.split(".", 1)[-1]
                    # Save discovered details
                    utils.emailServer = server
                    utils.emailDomain = domain
                    servers = [server]
                else:
                    verboseCasual.write( " * No Mail Server found!\n")
                    raise Exception( "No Mail Server")

        # Complete From Address setup
        if not fromDomain:
            fromDomain = domain

        # Setup Login user, if required
        if not userName:
            userName = fromAddr

        fromAddr = aliasString.format( fromAddr, fromDomain)
        msg[ "From"] = fromAddr
        if noReplyTo:
            msg[ "Reply-To"] = "NoReply@" + fromDomain

        # Setup Subject
        if subject:
            msg[ "Subject"] = subject

        # Setup Importance and Sensitivity
        for var, name, opts in [[ importance, "Importance", ["low", "high"]], [ sensitivity, "Sensitivity", ["personal", "private", "company-confidential"]]]:
            if var and isinstance( var, basestring):
                var = "{0}  ".format( var)[0:2].strip()  # v.1.9.0, Limit testing to first two characters!
                for item in opts:
                    if item.startswith( var.lower()):
                        msg[ name] = item
                        break

        # Add Preamble text for source origin details
        msg[ "Preamble"] = "Generated by ALFlib.py, v{0}.{1}.{2}, originating from '{3}'".format( utils.major, utils.minor, utils.bug, fqdn)

        # Try connecting and sending email repeated times if necessary
        retry = 0
        while tries:
            try:
                if retry:
                    verboseCasual.write( "\n - Send attempt #{0}\n".format( retry + 1))

                for index, server in enumerate( servers):
                    try:
                        server = server.strip()
                        if len( servers) > 1:
                            verboseCasual.write( " - Trying Server: '{0}'\n".format( server))

                        # Should we delay between send attempts?
                        if delay and (index or retry):
                            verboseDetail.write( " - Waiting {0} second delay...\n".format( delay))
                            time.sleep( delay)

                        # Make connection
                        if not connected:
                            smtp.connect( server, port)

                        # Perform Login attempt
                        if password:
                            try:
                                smtp.login( userName, password)

                            except Exception as e:
                                if "AUTH extension not supported" in str( e):
                                    verboseCasual.write( " * Authentication NOT required *\n")
                                    verboseDetail.write( "   Auth error: '{0}'\n".format( e))
                                else:
                                    raise

                        # Setup and verify Recipients list
                        toList = []
                        for title, addresses in [["To", toAddr], ["CC", ccAddr], ["BCC", bccAddr]]:
                            if addresses:
                                if isinstance( addresses, basestring):
                                    if "," in addresses:
                                        addresses = addresses.split( ",")
                                    else:
                                        addresses = addresses.split( ";")

                                msg[ title] = ", ".join( addresses)
                                # If not already included, append address to send list
                                for addr in addresses:
                                    if addr and addr not in toList:
                                        toList.append( addr)
                                        # Verify recipient
                                        vCode, vMsg = smtp.verify( addr)
                                        if vCode != 250:    	# Verification OK
                                            if vCode == 550:    # Unknown address
                                                verboseCasual.write( " * Unknown recipient: <{0}> *\n".format( addr))
                                            verboseDetail.write( " * Code {0} - <{1}>...{2} *\n".format( vCode, addr, vMsg))

                        verboseCasual.write( " - 'sendEmail' Sending: ")

                        smtp.sendmail( fromAddr, toList, msg.as_string( False))
                        verboseCasual.write( "Success!\n")
                        if details:
                            return {"Attempt": retry + 1, "Server": server}
                        return True
                    except Exception as e:
                        verboseDetail.write( " * Failed with error: {0}\n".format( e))
                        if index + 1 == len( servers):
                            verboseCasual.write( " * Send Failed!\n")
                            raise
                        verboseCasual.write( " * Send Failed, trying alternate Server...\n")

            except:
                tries -= 1
                if not tries:
                    if retry:
                        verboseCasual.write( "\n * Retries exhausted, giving up!\n")
                    raise
                retry += 1

    except:
        verboseCasual.write( "Failure!\n")
        raise

    finally:
        try:
            # Clean up any remaining connections
            smtp.quit()
        except:
            pass

##################################
# Handle display of script usage #
##################################

def _showInventory():
    """Internal function, not intended for general consumption!"""
    #import inspect

    availableClasses = []
    availableFunctions = []
    availableProperties = []
    members = {}

    for name, item in inspect.getmembers( utils):
        name = name.lower()
        if not name.startswith( "_"):
            if inspect.isclass( item):
                availableClasses.append( name)
                members[ name] = item
            elif inspect.isfunction( item):
                availableFunctions.append( name)
                members[ name] = item
            elif not inspect.ismodule( item):
                availableProperties.append( name)
                members[ name] = item

    verbose = False
    focus = False
    option = False

    for index in range( 1, len(sys.argv), 1):
        option = sys.argv[index]
        if option == '-h':
            verbose = True
            option = False
        else:
            option = option.lower()
            if verbose:
                focus = option
                verbose = False
            elif option in availableFunctions:
                args = ""
                for idx in range( index+1, len(sys.argv), 1):
                    if args:
                        args = args + ", " + sys.argv[idx]
                    else:
                        args = sys.argv[idx]
                try:
                    print( eval( "{0}( {1})".format( members[ option].__name__, args)))
                    return
                except Exception as e:
                    print( "\n\a * Exception calling Function '{0}': {1}".format( members[ option].__name__, e))
                    print( "   Check arguments! Forget to double-encapsulate strings?")
                    break
            elif option in availableProperties:
                try:
                    print( members[ option])
                    return
                except Exception as e:
                    print( "\n\a * Exception calling Property '{0}': {1}".format( option, e))
                    break

    scriptName = os.path.split( __file__)[1]
    title = "\n{0}, {1}:".format( scriptName, version()['Desc'])

    print( title)
    print( "-" * (len(title) - 1))

    if verbose:
        print( "\nAvailable Classes and Functions:")
    else:
        if option and option not in members:
            print( "\n * Unknown Function '{0}', please try again!\n".format( option))

        print( "\nFor additional Help detail:")
        print( "   Use: '{0} -h [<name>]'".format( scriptName))
        print( "\nTo execute a Function call:")
        print( "   Use: '{0} <func_name> [<param>[ <param>[ ...]]]'".format( scriptName))
        print( "    Ex: {0} getDownload \"'ftp://my.server.domain/test.dat'\"\n        userName=\"'me'\" password=\"'myself'\"".format( scriptName))
        print( "   (don't forget to double-encapsulate strings with quotes! Like \"'MyString'\")")
        print( "\nTo return a Property value:")
        print( "   Use: '{0} <prop_name>'".format( scriptName))

    for cat, cats, availableList in [["Class", "Classes", availableClasses], ["Function", "Functions", availableFunctions], ["Property", "Properties", availableProperties]]:
        if not verbose:
            print( "\n        Available {0}:\n".format( cats))

        for name in availableList:
            if availableList == availableProperties:
                help = getattr( utils, "_" + name + "__doc__", "{0}: {1}".format( cat, name))
            else:
                help = members[ name].__doc__

            if not help:
                help = "{0}: {1}()\n * Help is not available *".format( cat, members[ name].__name__)

            if verbose or name == focus:
                print( "\n-----")
                print( help)
            else:
                print( help.split('\n')[0])

if __name__ == "__main__":
    _showInventory()
