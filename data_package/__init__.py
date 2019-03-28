# coding = utf8
import pcap

# 抓包工具 - 待完成
# OSError: en0: You don't have permission to capture on that device ((cannot open BPF device) /dev/bpf0: Permission denied)
# 运行 sudo chmod 777 /dev/bpf* 开启网卡

def catch_data():
    pc = pcap.pcap("en0")
    pc.setfilter('tcp port 80')
    for ptime, pdata in pc:
        print(ptime, pdata)


catch_data()
