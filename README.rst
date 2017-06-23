****************************************
Misfortune cookie vulnerability analysys
****************************************

This is an analysis of a vulnerability (`CVE-2014-9222 <https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9222>`_) found by Check Point in an HTTP server firmware that runs on many home modems, their `report <http://mis.fortunecook.ie/>`_ states:

::

	This severe vulnerability allows an attacker to remotely
	take over the device with administrative privileges.

Alought the bug that causes the problem has been fixed many years ago, a recent `scan in Argentina <./scan>`_ reveals that the vulnerable version of the HTTP server is still deployed on nearly 220.000 devices (mainly belonging to Telecom Argentina).

The bug was presented in a `CCC talk <https://www.youtube.com/watch?v=W455bd6js0s>`_ by Lior Oppenheim and Shahar Tal. Other analysis of the bug worth reading are:

* http://cawanblog.blogspot.com.ar/2015/02/misfortune-cookie-cve-2014-9222.html
* https://www.nccgroup.trust/globalassets/our-research/uk/whitepapers/2015/10/porting-the-misfortune-cookie-exploit-whitepaper.pdf
