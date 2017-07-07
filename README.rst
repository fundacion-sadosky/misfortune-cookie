********************************************
Assessment of Misfortune Cookie in Argentina
********************************************

This is an assessment of the `Misfortune Cookie vulnerability <http://mis.fortunecook.ie/>`_ (`CVE-2014-9222 <https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9222>`_) found by Check Point in an HTTP server firmware that runs on many home modems, their report states:

::

	This severe vulnerability allows an attacker to remotely
	take over the device with administrative privileges.

Although the bug that causes the problem has been fixed many years ago, a recent `scan in Argentina <./scan>`_ revealed that the vulnerable version of the HTTP server (``RomPager/4.07``) is still deployed on nearly 220.000 devices (mainly belonging to Telecom Argentina S.A. in the non-standard port 30005).

The bug was presented in a `CCC talk <https://www.youtube.com/watch?v=W455bd6js0s>`_ by Lior Oppenheim and Shahar Tal. Other analysis of the bug worth reading are:

* `Misfortune Cookie (CVE-2014-9222) Demystified <http://cawanblog.blogspot.com.ar/2015/02/misfortune-cookie-cve-2014-9222.html>`_ by cawan
* `Porting the Misfortune Cookie Exploit: A Look into Router Exploitation Using the TD-8817 <https://www.nccgroup.trust/globalassets/our-research/uk/whitepapers/2015/10/porting-the-misfortune-cookie-exploit-whitepaper.pdf>`_ by Grant Willcox

This repository contains a directory with the `Python source code to reproduce the scan <./src/scan>`_ and in `another directory <./scan>`_ the instructions to use it, including `SQL code <./scan#sqlite>`_ to inspect the scan results saved in an anonymised `data base  <https://github.com/programa-stic/misfortune-cookie-analysis/releases/download/0.1.0/scan.sqlite.tar.gz>`_.

-----

**********************************************
Relevamiento de Misfortune Cookie en Argentina
**********************************************

Este es un relevamiento de la vulnerabilidad llamada `Misfortune Cookie <http://mis.fortunecook.ie/>`_ (`CVE-2014-9222 <https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9222>`_) descubierta por Check Point en el firmware que implementa un servidor HTTP que corre en muchos modems hogareños, su reporte dice:

::

	Esta vulnerabilidad severa permite a un atacante tomar el control
	del dispositivo con permisos de administrador en forma remota.

Aunque el bug que causa el problema fue arreglado hace ya varios años, recientemente realizamos un `scan en Argentina <./scan>`_ que reveló que la versión vulnerable del servidor HTTP (``RomPager/4.07``) todavía sigue siendo usada en casi 220.000 dispositivos (pertenecientes principalmente a Telecom Argentina S.A. en el puerto no estándar 30005).

El bug fue presentado en una `charla del CCC <https://www.youtube.com/watch?v=W455bd6js0s>`_ por Lior Oppenheim y Shahar Tal. Otros análisis del bug que valen la pena leer son:

* `Misfortune Cookie (CVE-2014-9222) Demystified <http://cawanblog.blogspot.com.ar/2015/02/misfortune-cookie-cve-2014-9222.html>`_ por cawan
* `Porting the Misfortune Cookie Exploit: A Look into Router Exploitation Using the TD-8817 <https://www.nccgroup.trust/globalassets/our-research/uk/whitepapers/2015/10/porting-the-misfortune-cookie-exploit-whitepaper.pdf>`_ por Grant Willcox

Este repositorio contiene un directorio con el `código Python para reproducir el scan <./src/scan>`_ realizado y en `otro directorio <./scan>`_ las instrucciones de cómo utilizarlo, incluyendo el `código SQL <./scan#sqlite>`_ para inspeccionar los resultados del scan almacenados en una `base de datos  <https://github.com/programa-stic/misfortune-cookie-analysis/releases/download/0.1.0/scan.sqlite.tar.gz>`_ anonimizada.
