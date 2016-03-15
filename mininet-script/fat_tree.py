from mininet.topo import Topo
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.net import CLI
from mininet.node import RemoteController


class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        # core switch
        core_sw_1 = self.addSwitch('s1001')
        core_sw_2 = self.addSwitch('s1002')
        core_sw_3 = self.addSwitch('s1003')
        core_sw_4 = self.addSwitch('s1004')

        # core switch
        for i in range(1, 5, 1):  # 1~4
            left_ag_sw = self.addSwitch('s200' + str(2*i-1))
            right_ag_sw = self.addSwitch('s200' + str(2*i))
            self.addLink(core_sw_1, left_ag_sw, bw=1000, loss=20)
            self.addLink(core_sw_2, left_ag_sw, bw=1000, loss=20)
            self.addLink(core_sw_3, right_ag_sw, bw=1000, loss=20)
            self.addLink(core_sw_4, right_ag_sw, bw=1000, loss=20)
            self.pod_generate(left_ag_sw, right_ag_sw, i-1) # pod_index: 0~3

    def pod_generate(self, left_ag_sw, right_ag_sw, pod_index):
        # edge switch
        left_edge_sw = self.addSwitch('s300' + str(2*pod_index+1))
        right_edge_sw = self.addSwitch('s300' + str(2*pod_index+2))

        # host
        h1 = self.addHost('h' + str(pod_index) + '1')
        h2 = self.addHost('h' + str(pod_index) + '2')
        h3 = self.addHost('h' + str(pod_index) + '3')
        h4 = self.addHost('h' + str(pod_index) + '4')

        # ag -> edge
        self.addLink(left_ag_sw, left_edge_sw, bw=100)
        self.addLink(left_ag_sw, left_edge_sw, bw=100)
        self.addLink(left_ag_sw, right_edge_sw, bw=100)
        self.addLink(right_ag_sw, left_edge_sw, bw=100)
        self.addLink(right_ag_sw, right_edge_sw, bw=100)

        # edge -> host
        self.addLink(left_edge_sw, h1, bw=100)
        self.addLink(left_edge_sw, h2, bw=100)
        self.addLink(right_edge_sw, h3, bw=100)
        self.addLink(right_edge_sw, h4, bw=100)

def test():
    topo = MyTopo()
    net = Mininet(topo=topo,
                  link=TCLink,
                  controller=None)
    # net.addController('c0',
    #                   controller=RemoteController,
    #                   ip='127.0.0.1',
    #                   port=6633)
    net.start()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    test()


topos = {'mytopo': (lambda: MyTopo())}
# sudo mn --custom mininet-script/fat_tree.py --topo mytopo --link=tc
