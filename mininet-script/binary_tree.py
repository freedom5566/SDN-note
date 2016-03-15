from mininet.topo import Topo
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.net import CLI


class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        self.hostNum = 1
        self.switchNum = 1
        root = self.addSwitch('s' + str(self.switchNum))
        self.switchNum += 1
        self.binary_tree(root, 3)

    def binary_tree(self, root, depth):
        if depth > 1:
            # switch
            nodeL = self.addSwitch('s' + str(self.switchNum))
            self.switchNum += 1
            nodeR = self.addSwitch('s' + str(self.switchNum))
            self.switchNum += 1
            self.addLink(root, nodeL, bw=1)
            self.addLink(root, nodeR, bw=1)
            self.binary_tree(nodeL, depth-1)
            self.binary_tree(nodeR, depth-1)
        else:
            # host
            nodeL = self.addHost('h' + str(self.hostNum))
            self.hostNum += 1
            nodeR = self.addHost('h' + str(self.hostNum))
            self.hostNum += 1
            self.addLink(root, nodeL, bw=10)
            self.addLink(root, nodeR, bw=10)


def test():
    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    test()


topos = {'mytopo': (lambda: MyTopo())}
# sudo mn --custom mininet-script/binary_tree.py --topo mytopo --link=tc
