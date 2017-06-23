*********************
Scan of Argentina IPs
*********************

Using the `masscan <https://github.com/robertdavidgraham/masscan>`_ tool, a scan for the vulnerable version of the RomPager server was done for all IPv4 argentian addresses, as reported from: 

http://www.ipdeny.com/ipblocks/data/countries/ar.zone

Nearly 220.000 HTTP servers were found that reported to have the vulnerable version, ``RomPager/4.07``. The big majority was found in a non standard port (30005), that corresponds to modems from Arnet (that is operated by Telecom Argentina).

From the search space of 19M addresses of the possible IPs that had been leased to argentina (desarrollar mejor, nombrar al LACNIC), the standard 7547 port and the non standard 30005 port where scanned, finding that 2.863.653 where open. Then a banner grabbing was performed to find the vulnerable version of the HTTP server (``RomPager/4.07``), reporting 220.738 devices with this vulnerable version.

All the logic is summarized in `main.py <../src/scan/main.py>`_.


Setup
-----

Ubuntu 14.04 with a 100Mbps connection.


Masscan
-------

With a clear documentation, the installation was performed according to the README without any issues.

::

	sudo ../masscan/bin/masscan -c scan/scan.conf

All the configuration options used are in the configuration file (including the IPs range) in `scan.conf <./scan.conf>`_.

A rate of 3000 packets per second (with 2 retries) was chosen, to balance scan speed with avoiding network saturation (the scan lasted several hours which was acceptable for the current target).


Banner grabbing
---------------

Masscan provides a banner grabbing feature but it didn't work as expected (missing many banners, probably due to a misconfiguration). The banner grabbing functionality was implemented with a custom python script using the requests package.


SQLite
------

All the results were parsed from the masscan generated xml file and stored in an database (``sqlite``).

To find the vulnerable devices:

.. code-block:: SQL

	SELECT * FROM scan where scan.http_banner like '%RomPager/4.07%'

	SELECT count(*) as Total, sum(port_7547) as "Port 7547", sum(port_30005) as "Port 30005",
	owner, country
	FROM
	(
	SELECT ip_blocks.inetnum, ip_blocks.country, ip_blocks.owner,
	ip_blocks.data, ip_blocks.ownerid, scan.ip_block_id,
	case scan.port when 7547 then 1 else 0 end as port_7547,
	        case scan.port when 30005 then 1 else 0 end as port_30005
	FROM scan INNER JOIN ip_blocks ON scan.ip_block_id == ip_blocks.id
	where scan.http_banner like '%RomPager/4.07%'
	)
	GROUP BY ownerid
	ORDER BY total DESC

	SELECT SUM(count) as count, *
	FROM
	(
	select count(*) as count, ip_blocks.inetnum, ip_blocks.country, ip_blocks.owner, scan.port, ip_blocks.data, ip_blocks.ownerid
	FROM scan INNER JOIN ip_blocks ON scan.ip_block_id == ip_blocks.id
	where scan.http_banner like '%RomPager/4.07%'
	group by ip_block_id
	) GROUP BY ownerid ORDER BY count DESC
