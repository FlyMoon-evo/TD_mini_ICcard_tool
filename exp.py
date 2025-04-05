import sys
import random

def calculate_xor_checksum(data_bytes):
    """计算 XOR 校验码"""
    checksum = 0
    for byte in data_bytes:
        checksum ^= byte
    return hex(checksum)[2:]

def calculate_sum_checksum(data_bytes):
    """计算累加和校验码"""
    sum_result = 0
    for byte in data_bytes:
        sum_result += byte
    return sum_result & 0xff

def hex_to_little_endian(hex_string):
    """将大端的16进制字符串转换为小端序列"""
    byte_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    return ''.join(byte_pairs[::-1])

# 获取输入参数
money = sys.argv[1]
use_num = random.randint(0, 0xff) if len(sys.argv) < 3 else int(sys.argv[2])

# 处理金额
money_val = int(float(money) * 100)
money_hex = hex(money_val)[2:]
money_hex = money_hex.zfill(6 if money_val > 0xffff else 4)  # 自动判断字节长度
money_bytes = bytes.fromhex(money_hex)

# 处理使用次数
use_num_hex = hex(use_num)[2:]

# 计算校验码
sum_checksum = calculate_sum_checksum(money_bytes)
inv_sum_checksum = hex(0xff - sum_checksum)[2:]
sum_checksum = hex(sum_checksum)[2:]

# 构建数据块
partial_data_block = f"00{use_num_hex}0000{use_num_hex}00000000{inv_sum_checksum}00{money_hex}{sum_checksum}"
partial_bytes = bytes.fromhex(partial_data_block)

# 计算最终校验码
xor_checksum = calculate_xor_checksum(partial_bytes)
inv_sum_checksum_2 = hex(0xff - calculate_sum_checksum(partial_bytes))[2:]

# 生成结果
result = hex_to_little_endian(f"{inv_sum_checksum_2}{partial_data_block}{xor_checksum}")
print(result)