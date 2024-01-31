import torch
from torch import nn
from torch.utils.data import DataLoader
from utils.data_set import MyDataSet


class Client(object):  # 定义客户端类
    def __init__(self, args, dataset=None, idxs=None):
        self.args = args  # 超参（字典？）
        self.loss_func = nn.CrossEntropyLoss()  # 交叉熵损失
        self.selected_clients = []
        self.ldr_train = DataLoader(MyDataSet(dataset, idxs),  # 下载数据集
                                    batch_size=self.args.local_bs,  # 批次大小
                                    shuffle=True)  # 随机化（每次迭代都会打乱数据集）

    def train(self, net):
        net.train()
        # train and update，梯度下降
        optimizer = torch.optim.SGD(net.parameters(), lr=self.args.lr, momentum=self.args.momentum)

        epoch_loss = []
        for iter in range(self.args.local_ep):
            batch_loss = []
            for batch_idx, (images, labels) in enumerate(self.ldr_train):  # 遍历ldr_train数据加载器
                images, labels = images.to(self.args.device), labels.to(self.args.device)
                net.zero_grad()  # 清除梯度
                log_probs = net(images)  # 训练数据
                loss = self.loss_func(log_probs, labels)  # 调用自定义的损失函数
                loss.backward()  # 反向传播
                optimizer.step()  # 参数更新
                if self.args.verbose and batch_idx % 10 == 0:
                    print('Update Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        iter, batch_idx * len(images), len(self.ldr_train.dataset),
                              100. * batch_idx / len(self.ldr_train), loss.item()))
                batch_loss.append(loss.item())
            epoch_loss.append(sum(batch_loss) / len(batch_loss))
        return net.state_dict(), sum(epoch_loss) / len(epoch_loss)  # 保存模型参数
