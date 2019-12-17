"""gen_cond_example.py: generate fv_for_examples"""

import argparse
import hashlib
import os
import random
import string
import sys
import json
import cond_template as templates

DEFAULT_OUTDIR = r"work_directory"

DEFAULT_METADATA_FILE = r"work_directory/manifest.json"

# 最多生成多少变量
MAX_NUM_VARS = 20

# 变量名模板
VAR_STR = "var_%s"

# 数组最大长度
MAX_IDX = 100

# 文件名hash后的字节长度
FNAME_HASHLEN = 5

# 命令行参数默认值

# 默认生成文件个数
DEFAULT_NUM_INSTANCES = 10

# 随机种子
DEFAULT_SEED = 0


def gen_cond_example():
    """Generate conditional example

    Returns:
        instance_str (str): str of code example
        tags (list of Tag): tag for each line representing buffer safety
    """
    # 生成10个随机的变量名
    anon_vars = _get_anon_vars()
    # 给模板中所有的变量赋值
    array_var, lcmp_var, rcmp_var = anon_vars[:3]  # 获取前三个变量名 缓存变量，索引变量 阈值变量
    array_len = random.randrange(MAX_IDX)  # 随机获取一个缓存的长度
    lcmp_init = random.randrange(MAX_IDX)  # 随机获取一个初始索引
    rcmp_init = random.randrange(MAX_IDX)  # 随机获取一个合法阈值索引
    true_idx = random.randrange(MAX_IDX)  # 正确的索引
    false_idx = random.randrange(MAX_IDX)  # 错误的索引
    substitutions = {
        'array_var': array_var,  # 缓存变量
        'lcmp_var': lcmp_var,  # 索引变量即为最终索引的索引值
        'array_len': array_len,  # 缓存长度
        'rcmp_init': rcmp_init,  # 阈值
        'rcmp_var': rcmp_var,  # 阈值变量
        'lcmp_init': lcmp_init,  # 初始索引
        'true_idx': true_idx,  # 正确索引
        'false_idx': false_idx  # 错误索引
    }

    # 主条件语句模板
    main_lines = templates.COND_MAIN_LINES

    # 条件语句声明和初始化模板
    dec_init_pairs = templates.COND_DEC_INIT_PAIRS

    # 进一步整合汇聚
    # 获得声明初始化代码列表，这样做是为了让每一行只有一条语句
    setup_lines = _get_setup_lines(dec_init_pairs)
    lines = setup_lines + main_lines
    instance_str = _get_instance_str(lines, substitutions, templates.FUNC_TMPL_STR)  # 对模板进行替换。
    return instance_str


# 返回MAX_NUM_VARS个变量名
def _get_anon_vars():
    """生成变量名
    Returns:
        anon_vars (list of str)
    """
    anon_vars = [VAR_STR % itm for itm in range(MAX_NUM_VARS)]  # VAR_STR是变量名模板
    random.shuffle(anon_vars)
    return anon_vars


# 将声明和定义语句对排好。因为字符数组只声明，不赋值。则用None表示
def _get_setup_lines(dec_init_pairs):
    """变量定义及初始化

    Args:
        dec_init_pairs (list of tuple)

    Returns:
        setup_lines (list of str)
    """
    setup_lines = []
    for (dec_str, init_str) in dec_init_pairs:
        if init_str is None:  # 表明是个数组声明模板 可以随机插入到任意一行
            idx = random.randrange(len(setup_lines) + 1)
            setup_lines = setup_lines[:idx] + [dec_str] + setup_lines[idx:]  # 因为是只声明，所以可以直接插入进来。
        else:
            idxes = sorted(  # 表明既有声明，又有初始化，则需要随机选择两个位置，而且要从小到大进行排序
                [random.randrange(len(setup_lines) + 1) for _ in range(2)])
            # 插入这两个特定的位置，先插入声明语句，再插入赋值语句
            setup_lines = (setup_lines[:idxes[0]] + [dec_str] +
                           setup_lines[idxes[0]:idxes[1]] + [init_str] +
                           setup_lines[idxes[1]:])

    return setup_lines


def _get_instance_str(lines, substitutions, func_tmpl_str):
    """Make substitutions and construct function instance string

    Args:
        lines (list of str): lines in body, to be substituted
        substitutions (dict)
        func_tmpl_str (str): string for function template to substitute
        tags (list of Tag)
        tags_as_comments (bool): if True, then add the tag as a comment at the
            end of each line

    Returns:
        instance_str (str): complete function as string
    """
    lines = [string.Template(itm).substitute(substitutions) for itm in lines]  # 将所有模板代码语句进行替换
    body = "\n".join("    " + line for line in lines)  # 对body进行重新赋值
    substitutions['body'] = body
    instance_str = string.Template(func_tmpl_str).substitute(substitutions)
    return instance_str


def _get_args():
    """Get command-line arguments 返回从命令行解析之后的参数"""
    separator = '\n' + "#" * 79 + '\n'
    parser = argparse.ArgumentParser(
        description=__doc__ + separator,
        formatter_class=argparse.RawDescriptionHelpFormatter)  # 描述已经正确排好格式
    parser.add_argument('-num',
                        help=("(int) Number of instance.c files to create; default "
                              "{}".format(DEFAULT_NUM_INSTANCES)),
                        default=DEFAULT_NUM_INSTANCES,
                        metavar="<int>")

    parser.add_argument('-seed',
                        help=("(int) Seed for random number generator, to reproduce results; "
                              "default {}. If -1 is passed, then use default Python "
                              "seed".format(DEFAULT_SEED)),
                        default=DEFAULT_SEED,
                        metavar="<int>")

    args = parser.parse_args()
    return args  # 返回从命令行解析之后的参数


def _generate_file_name(instance_str):
    """generate filename according to instance_str"""
    byte_obj = bytes(instance_str, 'utf-8')
    fname = hashlib.shake_128(byte_obj).hexdigest(FNAME_HASHLEN)
    fname = "{}.cpp".format(fname)
    return fname


def main(args):
    """With fixed initial seed, generate instances and save as C files

    Args:
        args (argparse.Namespace), with attributes:
            num_instances (int): how many instances to generate
            outdir (str): path to directory to save instances; must exist
            seed (int): seed to use for random.seed(). If -1, then seed by
                default Python seeding

    Returns: 0 if no error
    """

    # check outdir paths
    outdir = DEFAULT_OUTDIR
    outdir = os.path.abspath(os.path.expanduser(outdir))
    if not os.path.isdir(outdir):  # 判断路径是否为目录
        raise OSError("outdir does not exist: '{}'".format(outdir))

    # set seed
    seed = int(args.seed)
    if seed != -1:
        random.seed(seed)

    file_set = []  # store instance tag metadata
    inst_num = 0
    num_instances = int(args.num)
    while inst_num < num_instances:
        # generate example
        instance_str = gen_cond_example()

        # generate filename by instance_str
        fname = _generate_file_name(instance_str)
        if fname in file_set:  # 如果刚好生成的两个文件名一样，那就说明这两个文件是一样的。
            # Collision, try again
            continue
        else:
            file_set.append(fname)

        # write instance_str to file
        path = os.path.join(outdir, fname)
        with open(path, 'w') as f:
            f.write(instance_str)

        inst_num += 1

    # Generate metadata only if the metadata_file argument is present
    generate_metadata = DEFAULT_METADATA_FILE is not None
    if generate_metadata:
        # construct the complete metadata
        metadata = {
            "working_dir": outdir,
            "num_instances": num_instances,
            "files": file_set
        }
        with open(DEFAULT_METADATA_FILE, 'w') as f:
            json.dump(metadata, f)

    return 0


if __name__ == '__main__':
    RET = main(_get_args())
    sys.exit(RET)
    # python3.6 sa_babi/gen_cond_example.py work_directory -seed 0 -num_instances 10 -metadata_file work_directory/manifest.json
    # clang + + -S - emit - llvm - std = c + +11 - O3 - ffast - math - march = native a_0.c - o a.ll
