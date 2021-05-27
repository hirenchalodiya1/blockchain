import requests

P_KEY = "3082025c020100028181008a1a0c54c8599dcc842003d0fcd3edab296e197d0dc6deee1d697e796db8aa02c0cdfa9ab56ba660d86f63d9d8be7743ab1e644269ee0a7f3e5e684bc2b851bae06655ab8b6e98d63cdb51c30bfe6a54c9dde5fa002aa7af1891956de1cc918308d2f1d0292d0c7a21a982408c2367869d28f97e20585fe0db59dedadecefd8d02030100010281800a2010c9628b1783b82834bf6cda08f1e4aebad5ad5de85862f5aa1d330b3803cda90c77ad578032578c0b311cb0124476d65a9977f4c8f63d5764a431599c3c50c524f9a656f474c38923eab4b9638b64f1f17eea5152821a7cb91eb1d5ee9ed5ea8e5d22ffac9e5fff03426e067371405074f9762365f64681fc1236cb2781024100b786c80f64d577031ee2dbb379209cdebaa981835dc931986c923d3723594a7dde7cb9f468f71c8d3bfd43cde71ee0bb2227223f835e5b1ec749221594a0a0ed024100c0a32650b14d2b37708e6a073a6b8f82b6a38f4e6b62a4862ec01fee20ed78f431c65a6618136efd8a557e76d6a02df17b05d23da5ef4ded0c6ecb9241be5b21024100843e62ba74f63ca3cb05bd3a3df5fa13a47db00d70ef2105ac765415ff2ac03aa2af4d6f889347c79d8a89e93cb94b468cfd95f81e39477f8e2a6c9d10540ea10240402d9ab4437d9c2a4a3b882384591564cd084cd4297ea1a57aa9d379784ae583259a19bfedc17bb6c88197326c6acd23a882d5fa67f0041c378a2a143e06f74102406f1b2aa18a554c31cae061656000968da225f1d0446f15e98bc43d882a87ff0654416adeb23d3ad114310fe96446a807567eacf60bd1133fdc0c5ac0510cbe2a"


class NodeHandler:
    current_port = 5000
    current_url = "http://localhost:5003"

    total_nodes = None
    ACTIONS = {
        0: "Change Node",
        1: "Display current node",
        2: "Create Wallet",
        3: "Transaction"
    }

    def take_inputs(self, inputs):
        ret = {}
        for i in inputs:
            ret[i] = input(f"Enter {i}: ")
        return ret.values()

    def print_action(self):
        for key, value in self.ACTIONS.items():
            print(f"{key}. {value}")

    def create_wallet(self):
        name, username, email = self.take_inputs(['name', 'username', 'email'])
        data = {
            'name': name,
            'username': username,
            'email_id': email
        }
        response = requests.get(self.current_url + '/wallet/new', data=data)
        if response.status_code != 200:
            print("Error: " + response.text)
        else:
            print("Private key:", response.json()['private_key'])

    def transact(self):
        sender = "e"
        key = P_KEY

        data = {
            'sender': sender,
            'private_key': P_KEY,
            'message': "This is test 23"
        }

        response = requests.post(self.current_url + '/message/send', data=data)
        if response.status_code != 200:
            print("Error: " + response.text)
        else:
            print("Signature:", response.json()['signature'])

    def take_action(self):
        if self.current_port is None:
            self.current_port = str(int(input("Enter port number of node: ")))
        self.current_url = f"http://localhost:{self.current_port}"

        self.print_action()

        action = input("Your Choice: ")

        if action == "0":
            self.current_port = None
        elif action == "1":
            print(self.current_url)
        elif action == "2":
            self.create_wallet()

    def handle(self):
        try:
            while True:
                self.take_action()
        except (KeyboardInterrupt, EOFError):
            exit(0)


if __name__ == "__main__":
    handler = NodeHandler()
    # handler.handle()
    # handler.create_wallet()
    handler.transact()
