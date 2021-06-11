# -*- coding: utf-8 -*- 
# @Time : 2021/5/13 13:37
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : comment.py 
# @Software: PyCharm


import random

from server.tool import load_json

opcode_mapping = {'event_whenflagclicked': '【当绿旗被点击】',
				  'motion_gotoxy': '【移动到(x,y)】',
				  'motion_movesteps': '【移动x步】',
				  'control_forever': '【重复执行】',
				  'control_if': '【如果那么】',
				  'sensing_touchingobject': '【碰到xx】',
				  'motion_pointtowards': '【面向xx】',
				  'control_stop': '【停止xx】',
				  'motion_glidesecstoxy': '【在x秒内滑行到(x,y)】',
				  'motion_pointindirection': '【面向xx方向】',
				  'event_whenkeypressed': '【当按下xx键】',
				  'control_repeat': '【重复执行x次】',
				  'motion_goto': '【移到xx】',
				  'looks_switchcostumeto': '【换成xx背景】',
				  'looks_costume': '【xx背景】',
				  'looks_hide': '【隐藏】',
				  'looks_show': '【显示】',
				  'control_wait': '【等待】', }

# 开头
supply_option1 = ["亲爱的小朋友，收到你的作品老师非常的惊喜，看起来你已经对图形化编程的世界理解的相当透彻了。",
				  "亲爱的小朋友，收到你的作品老师非常的惊喜，虽然你才刚刚接触图形化编程世界，但是你已经能够理解它的一部分奥秘了。",
				  "亲爱的小朋友，是不是不小心提交没有完成的作业呢？仔细检查一下，完成之后再让老师看看你的精心设计吧。"]

# 逻辑性
supply_option2 = "你拥有很强的逻辑思维。"

# 复杂度 >16
supply_option3 = ["小朋友是不是把问题想的太复杂了呢？仔细想想有没有其他的解决办法呢？",
				  "小朋友尝试着优化一下作品，能不能用更少的代码块达到现在作品的效果。"]

# 工作量
supply_option4 = "你并没有满足于完成任务本身，而是做了很多尝试。"

# 创新
supply_option5 = ["你尝试添加了更多新的角色", "你尝试使用了更多的角色"]

# 结尾
supply_option6 = ["接下来我们还将一起设计更加有趣的作品，老师期待和你的下次见面，咱们不见不散(>‿<)",
				  "加油吧，小朋友我们注定将设计出这世界上无比美妙的作品，接下来的学习中，希望你能够继续发挥自己的创造力，打造专属于你自己的图形化编程世界(●'‿'●)",
				  "加油吧，希望你能继续开拓自己的思维，给作品融入更多的个人印记，咱们下节学习不见不散，老师期待着你的新作品(•̀ω•́)✧"]


def generate_comment(filepath, score, logicality, workload, complexity, num_ir_roles, num_beast, num_bill):
	overall = "【作业质量】"
	knowledge = "【知识点使用情况】"
	supply = "【补充】"
	if score == 5:
		overall += "优秀"
		supply += supply_option1[0]
	elif score == 4 or score == 3:
		overall += "良好"
		supply += supply_option1[1]
	else:
		overall += "一般"
		supply += supply_option1[2]

	if logicality > 0.9:
		supply += supply_option2

	if complexity > 15:
		supply += supply_option3[0]
	elif 11 >= complexity > 16:
		supply += supply_option3[1]

	if workload > 48.61235702962293:
		supply += supply_option4

	if num_ir_roles > 0:
		overall += "+创新"
		supply += supply_option5[0]
	elif num_bill > 1 or num_beast > 1:
		overall += "+创新"
		supply += supply_option5[1]

	supply += supply_option6[random.randint(0, 2)]

	scode = load_json(filepath)
	targets = scode['targets']

	opcode_set = set()
	for e in targets:
		blocks = e['blocks']

		for k, v in blocks.items():
			try:
				opcode = v['opcode']
				opcode_set.add(opcode)
			except:
				pass

	opcode_list = list(opcode_set)
	for i in range(len(opcode_list)):
		opcode = opcode_list[i]
		if opcode in opcode_mapping.keys() and i == 0:
			knowledge += "对" + opcode_mapping[opcode]
		elif opcode in opcode_mapping.keys() and i > 0:
			knowledge += "、" + opcode_mapping[opcode]
	knowledge += "等知识点已经基本掌握。"

	comment = overall + "\\n" + knowledge + "\\n" + supply

	return comment