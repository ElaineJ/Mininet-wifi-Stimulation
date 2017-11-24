#!/usr/bin/python

'Setting the position of nodes'

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

def topology():

    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', position='70.0,50.0,0.0', 
			     ip='10.0.0.1/8',range=10)
    ap1 = net.addAccessPoint('ap1', ssid='ssid_ap1', mode='g', channel='1',
                             position='50,50,0',range='50')
    ap2 = net.addAccessPoint('ap2', ssid='ssid_ap2', mode='g', channel='1',
                             position='125,50,0',range='50',ip='10.8.8.8/8')
    ap3 = net.addAccessPoint('ap3', ssid='ssid_ap3', mode='g', channel='1',
                             position='175,50,0',range='50')
    c1 = net.addController('c1', controller=Controller)
    h1 = net.addHost ('h1', ip='10.0.0.3/8')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(ap1, h1)
    net.addLink(ap2, ap1)
    net.addLink(ap3, ap2)

    net.plotGraph(max_x=200, max_y=200)

    # Comment out the following two lines to disable AP
    print "*** Enabling association control (AP)"
    net.associationControl( 'ssf' )    


    net.startMobility(startTime=0)
    net.mobility(sta1, 'start', time=60, position='70.0,50.0,0.0')
    net.mobility(sta1, 'stop', time=150, position='200.0,50,0.0')
    net.stopMobility(time=151) 

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    
    print "*** Running CLI"
    CLI(net)


    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
