import re
from datetime import datetime, timedelta
import data


def check_input():
    while True:
        id_number = input('请输入身份证: ')
        if re.match(data.ID_NUMBER_18_REGEX, id_number):
            return id_number
            break
        else:
            print('输入错误！')


class Id:
    """分析18位身份证信息"""
    def __init__(self, id_number):
        self.id = id_number
        self.area_id = int(id_number[0:6])
        self.birth_year = int(id_number[6:10])
        self.birth_month = int(id_number[10:12])
        self.birth_day = int(id_number[12:14])

    def area_name(self):
        """根据区域编号取出区域名称"""
        return data.AREA_INFO[self.area_id]

    def birthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def age(self):
        """通过身份证号获取年龄"""
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def sex(self):
        """通过身份证号获取性别， 女生：0，男生：1"""
        if int(self.id[16:17]) % 2 == 0:
            return '女'
        else:
            return '男'

    def verify(self):
        """校验身份证是否正确"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        if check_digit == 10:
            check_digit = 'X'

        if str(check_digit) == self.id[-1]:
            return '正确'
        else:
            return '错误'

    def constellation(self):
        """获取星座信息"""
        month = self.birth_month
        day = self.birth_day

        start_date = data.get_constellation()[month]['start_date']
        start_day = int(start_date.split('-')[-1])

        if day < start_day:
            tmp_month = 12 if month - 1 == 0 else month - 1
            return data.get_dataellation()[tmp_month]['name']

        return data.get_constellation()[month]['name']

    def chinese_zodiac(self):
        """获取生肖"""
        start = 1900  # 子鼠
        end = self.birth_year
        key = (end - start) % 12
        return data.get_chinese_zodiac()[key]


if __name__ == '__main__':
    input_id = check_input()
    print('地址:', Id(input_id).area_name())
    print('生日:', Id(input_id).birthday())
    print('年龄:', Id(input_id).age())
    print('性别:', Id(input_id).sex())
    print('校验:', Id(input_id).verify())
    print('星座:', Id(input_id).constellation())
    print('生肖:', Id(input_id).chinese_zodiac())
