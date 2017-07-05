****************************************
Misfortune cookie vulnerability analysys
****************************************

This is an analysis of the `Misfortune Cookie vulnerability <http://mis.fortunecook.ie/>`_ (`CVE-2014-9222 <https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9222>`_) found by Check Point in an HTTP server firmware that runs on many home modems, their report states:

::

	This severe vulnerability allows an attacker to remotely
	take over the device with administrative privileges.

Although the bug that causes the problem has been fixed many years ago, a recent `scan in Argentina <./scan>`_ reveals that the vulnerable version of the HTTP server (``RomPager/4.07``) is still deployed on nearly 220.000 devices (in the non-standard port 30005, mainly belonging to Telecom Argentina S.A.).

The bug was presented in a `CCC talk <https://www.youtube.com/watch?v=W455bd6js0s>`_ by Lior Oppenheim and Shahar Tal. Other analysis of the bug worth reading are:

* `Misfortune Cookie (CVE-2014-9222) Demystified <http://cawanblog.blogspot.com.ar/2015/02/misfortune-cookie-cve-2014-9222.html>`_ by cawan
* `Porting the Misfortune Cookie Exploit: A Look into Router Exploitation Using the TD-8817 <https://www.nccgroup.trust/globalassets/our-research/uk/whitepapers/2015/10/porting-the-misfortune-cookie-exploit-whitepaper.pdf>`_ by Grant Willcox
