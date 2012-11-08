echo "3-ORD1"
ssh 10.0.3.21 " asn_cli.py -n pss_5298 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "5-MAA1"
ssh 10.0.5.22 " asn_cli.py -n pss_5059 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "6-DEL1"
ssh 10.0.6.21 " asn_cli.py -n pss_6495 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "7-BOM2"
ssh 10.0.7.21 " asn_cli.py -n pss_6328 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "8-BLR1"
ssh 10.0.8.21 " asn_cli.py -n pss_4634 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "9-LHR1"
ssh 10.0.9.21 " asn_cli.py -n pss_5533 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "10-DFW1"
ssh 10.0.10.21 " asn_cli.py -n pss_4686 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "11-ASH1"
ssh 10.0.11.21 " asn_cli.py -n pss_4600 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "12-SJC3"
ssh 10.0.12.21 " asn_cli.py -n pss_5025 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "13-HKG1"
ssh 10.0.13.21 " asn_cli.py -n pss_4720 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
echo "14-SHA1"
ssh 10.0.14.21 " asn_cli.py -n pss_5901 -c 'show tcp hosetable'"|tail -n 14
echo "-----------------------------------------------------------------------------"
