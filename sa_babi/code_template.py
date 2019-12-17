# 定义及初始化，每个元组有2个维度。第1个维度为声明语句，第2个维度为初始化语句
# ===================================程序主体===================================
CODE_TMPL_STR = """
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <iostream>
#include <stdio.h>
using namespace std;
int main()
{
$body
    return 0;
}"""
# ===================================随机语句===================================
RANDOM_MAIN_LINES = [
    "$random_var = $random_var_1 $random_opt $random_val;"
]
# ===================================条件分支===================================
CONDITION_DEC_INIT_PAIRS = [
    ("int $lcmp_var;", "$lcmp_var = $lcmp_init;"),
    ("int $rcmp_var;", "$rcmp_var = $rcmp_init;")
]

CONDITION_MAIN_LINES = [
    "if($lcmp_var < $rcmp_var){",
    "   $random_code_true",
    "} else {",
    "   $random_code_false",
    "}"
]
# ===================================输入输出===================================
IO_DEC_INIT_PAIRS = [
    ("char $out_var[$out_len] = \"$out_str\";", None),
    ("int $in_var;", None)
]

IO_MAIN_LINES = [
    "printf(\"%s\\n\",$out_var);",
    "cout << \"$out_var\" << str << endl;",
    "scanf(\"%d\",&$in_var);",
    "cin >> $in_var << endl;"
]
# ===================================函数调用===================================
FUN_DEC_INIT_PAIRS = [
    ("int $fun_name(int $fun_arg);", None)
]

FUN_MAIN_LINES = [
    "$fun_body",
    "return $fun_res"
]
# ===================================循环语句===================================
FOR_DEC_INIT_PAIRS = [

]
FOR_MAIN_LINES =[
    "for(int $for_var = 0; $for_var < $forcmp_var; $for_var++){",
    "   $for_body",
    "}"
]
