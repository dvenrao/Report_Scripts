#!/bin/sh

#ex. sjc=2,bom=4
POPID=12
#ex. sjc1,hkg1
POPNAME=sjc3
#ex. 3633 for pns_3633,pns_3633
NEXUSID=4799
###########################################
PNS=11
PSS=21
echo "############## PNS ##################"
IP=10.0.$POPID.$PNS
#################### max log settings ############################
ssh $IP "echo '<log_settings>
<schema>1</schema>
  <output>
    <for_filter>default</for_filter>
    <param>
      <name>max_file_size</name>
      <value>100m</value>
    </param>
  </output>
</log_settings>' > /var/aryaka/log_settings.xml"
echo "/var/aryaka/log_settings.xml"
#################### Controller ############################
ssh $IP "echo '<log_settings>
        <schema>1</schema>
        <filter>
                <name>warn</name>
                <level>warn</level>
                <output>warn</output>
        </filter>
       <output>
                <name>warn</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>warn_controller_"$POPNAME"_pns.log</value>
                </param>
        </output>

        <filter>
                <name>error</name>
                <level>error</level>
                <output>error</output>
        </filter>
       <output>
                <name>error</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>error_controller_"$POPNAME"_pns.log</value>
                </param>
        </output>

        <filter>
                <name>alert</name>
                <level>alert</level>
                <output>alert</output>
        </filter>
       <output>
                <name>alert</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>alert_controller_"$POPNAME"_pns.log</value>
                </param>
        </output>
</log_settings>' > /var/aryaka/controller/log_settings.xml"
echo "/var/aryaka/controller/log_settings.xml"
#################### ha_manager ############################
ssh $IP "echo '<log_settings>
        <schema>1</schema>
        <filter>
                <name>warn</name>
                <level>warn</level>
                <output>warn</output>
        </filter>
       <output>
                <name>warn</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>warn_ha_manager_"$POPNAME"_pns.log</value>
                </param>
        </output>

        <filter>
                <name>error</name>
                <level>error</level>
                <output>error</output>
        </filter>
       <output>
                <name>error</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>error_ha_manager_"$POPNAME"_pns.log</value>
                </param>
        </output>

        <filter>
                <name>alert</name>
                <level>alert</level>
                <output>alert</output>
        </filter>
       <output>
                <name>alert</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>alert_ha_manager_"$POPNAME"_pns.log</value>
                </param>
        </output>
</log_settings>' > /var/aryaka/ha_manager/log_settings.xml"
echo "/var/aryaka/ha_manager/log_settings.xml"

#################### ipsec PNS ############################
ssh $IP "echo '<log_settings>
        <schema>1</schema>
        <filter>
                <name>warn</name>
                <level>warn</level>
                <output>warn</output>
        </filter>
       <output>
                <name>warn</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>warn_ipsec_"$POPNAME"_pns.log</value>
                </param>
        </output>

        <filter>
                <name>error</name>
                <level>error</level>
                <output>error</output>
        </filter>
       <output>
                <name>error</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>error_ipsec_"$POPNAME"_pns.log</value>
                </param>
        </output>

        <filter>
                <name>alert</name>
                <level>alert</level>
                <output>alert</output>
        </filter>
       <output>
                <name>alert</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>alert_ipsec_"$POPNAME"_pns.log</value>
                </param>
        </output>
</log_settings>' > /var/aryaka/nexus/racoon/log_settings.xml"
echo "/var/aryaka/nexus/racoon/log_settings.xml"

#################### nexus PNS ############################

ssh $IP "echo '<log_settings>
        <schema>1</schema>
        <filter>
                <name>warn</name>
                <level>warn</level>
                <output>warn</output>
        </filter>
       <output>
                <name>warn</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>warn_pns_"$NEXUSID".log</value>
                </param>
        </output>

        <filter>
                <name>error</name>
                <level>error</level>
                <output>error</output>
        </filter>
       <output>
                <name>error</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>error_pns_"$NEXUSID".log</value>
                </param>
        </output>

        <filter>
                <name>alert</name>
                <level>alert</level>
                <output>alert</output>
        </filter>
       <output>
                <name>alert</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>alert_pns_"$NEXUSID".log</value>
                </param>
        </output>

        <filter>
                <name>info</name>
                <level>info</level>
                <output>info</output>
        </filter>
       <output>
                <name>info</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>info-pns_"$NEXUSID".log</value>
                </param>
        </output>

</log_settings>' > /var/aryaka/nexus/pns_"$NEXUSID"/log_settings.xml"
echo "/var/aryaka/nexus/pns_"$NEXUSID"/log_settings.xml"


echo "############## PSS #################"
IP=10.0.$POPID.$PSS
#################### max log settings ############################
ssh $IP "echo '<log_settings>
<schema>1</schema>
  <output>
    <for_filter>default</for_filter>
    <param>
      <name>max_file_size</name>
      <value>100m</value>
    </param>
  </output>
</log_settings>' > /var/aryaka/log_settings.xml"
echo "/var/aryaka/log_settings.xml"
#################### Controller ############################
ssh $IP "echo '<log_settings>
        <schema>1</schema>
        <filter>
                <name>warn</name>
                <level>warn</level>
                <output>warn</output>
        </filter>
       <output>
                <name>warn</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>warn_controller_"$POPNAME"_pss.log</value>
                </param>
        </output>

        <filter>
                <name>error</name>
                <level>error</level>
                <output>error</output>
        </filter>
       <output>
                <name>error</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>error_controller_"$POPNAME"_pss.log</value>
                </param>
        </output>

        <filter>
                <name>alert</name>
                <level>alert</level>
                <output>alert</output>
        </filter>
       <output>
                <name>alert</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>alert_controller_"$POPNAME"_pss.log</value>
                </param>
        </output>
</log_settings>' > /var/aryaka/controller/log_settings.xml"
echo "/var/aryaka/controller/log_settings.xml"
#################### nexus PSS ############################
ssh $IP "echo '<log_settings>
        <schema>1</schema>
        <filter>
                <name>warn</name>
                <level>warn</level>
                <output>warn</output>
        </filter>
       <output>
                <name>warn</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>warn_pss_"$NEXUSID".log</value>
                </param>
        </output>

        <filter>
                <name>error</name>
                <level>error</level>
                <output>error</output>
        </filter>
       <output>
                <name>error</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>error_pss_"$NEXUSID".log</value>
                </param>
        </output>

        <filter>
                <name>alert</name>
                <level>alert</level>
                <output>alert</output>
        </filter>
       <output>
                <name>alert</name>
                <type>rolling</type>
                <param>
                   <name>file</name>
                   <value>alert_pss_"$NEXUSID".log</value>
                </param>
        </output>
</log_settings>' > /var/aryaka/nexus/pss_"$NEXUSID"/log_settings.xml"
echo "/var/aryaka/nexus/pss_"$NEXUSID"/log_settings.xml"
