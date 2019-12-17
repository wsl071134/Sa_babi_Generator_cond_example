# 定义及初始化，每个元组有2个维度。第1个维度为声明语句，第2个维度为初始化语句

# ===================================程序主体===================================
FUNC_TMPL_STR = """
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
# ===================================条件分支===================================
COND_DEC_INIT_PAIRS = [
    ("char $array_var[$array_len];", None),
    ("int $lcmp_var;", "$lcmp_var = $lcmp_init;"),
    ("int $rcmp_var;", "$rcmp_var = $rcmp_init;")
]

COND_MAIN_LINES = [
    "if($lcmp_var < $rcmp_var){",
    "   $lcmp_var = $true_idx;",
    "} else {",
    "   $lcmp_var = $false_idx;",
    "}"
]

PRINT_LINES = ["printf(\"%d\\n\",$max_idx);", "cout << \"$out_str\" << str << endl;"]
SCANF_LINES = ["scanf(\"%d\",&$max_var);", "cin >>$in_str<< endl;"]

# "for($idx_var = $idx_init; $idx_var < $max_var; $idx_var++){",
# "   $s1_var[$idx_var]+= $sum_var;",
# "   $s1_var[$idx_var] = $s2_var[$idx_var]+$sum_var;",
# "   $s2_var[$idx_var+1] = $s1_var[$idx_var];"
# "   $s1_var[$idx_var+1] = $s3_var[$idx_var]+$s4_var[$idx_var];"
# "   $s4_var[$idx_var+1] = $s1_var[$idx_var]+$s2_var[$idx_var];"
# "   $s3_var[$idx_var+1] = $s2_var[$idx_var]+$s4_var[$idx_var];"
# "}"
