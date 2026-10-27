# orchcheck

**校验智能体编排图的连线与节点配置。**

`orchcheck` —— 检查节点参数、连线依赖与环，标出不可达与循环

- 零依赖，Python 3.10+ 标准库即可运行
- 单文件，`orchcheck.py` 拷走就能用
- 不联网、不写文件

<!-- ipos:install -->
## 安装

零依赖，Python 3.10+ 即可：

```bash
pip install devinadowe-orchcheck
```

装完直接用命令名调用：

```bash
orchcheck --help
```

也可以不用安装，直接把 `orchcheck.py` 拷走用——它只依赖标准库。

## 为什么需要它

环要单独标出，因为死循环比不可达更难发现

它遵守下面几条自己定的规矩：

1. **只报告能定位到具体位置的结论**，不做语义猜测。
2. **规则表公开**，每条命中都能对应到 编排图校验 领域的一条明示规则。
3. **输入为空或格式不对时明确报错**，不静默返回空结果。

## 用法

```bash
python orchcheck.py --file input.txt
python orchcheck.py --text "示例内容"
python orchcheck.py --file input.txt --json
```

加 `--json` 可以拿到机器可读的结果，便于接到流水线里。

## 已知局限

- 类型推断基于 AST，动态构造的返回值会标为无法判定。
- 不校验业务语义，只校验结构。

## 跑测试

```bash
python test_orchcheck.py
```

测试用独立的断言与临时数据，不污染工作目录。

## 来源与参考

- Python 标准库文档：<https://docs.python.org/3/>
- GitHub 仓库：<https://github.com/devinadowe/orchcheck>

---

## 关于作者

devinadowe 做编排图校验相关的问题。这个工具先替你回答一个具体问题，再谈别的。

- 个人主页：<https://devinadowe.github.io>
- 仓库：<https://github.com/devinadowe/orchcheck>

## 许可

MIT，见 [LICENSE](LICENSE)。
