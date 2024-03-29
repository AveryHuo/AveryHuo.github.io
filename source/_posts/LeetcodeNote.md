---
title: 力扣刷题记录
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1603943631534.png
categories:
- 算法
---

[toc]

## 1. 两数之和
* 1. Two Sum

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/two-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。

>示例:
给定 nums = [2, 7, 11, 15], target = 9
因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]

```c++
 vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> result;
        map<int, int> numsMap;
        
        for (int i = 0; i < nums.size(); i++)
        {
            int left = target - nums[i];

            if (numsMap.count(left) > 0) {
                result.push_back(numsMap[left]);
                result.push_back(i);
                break;
            }
            numsMap[nums[i]] = i;
        }

        return result;
    }
```

## 2.两数相加
* 2. Add Two Numbers
 
 来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/add-two-numbers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给出两个 非空 的链表用来表示两个非负的整数。其中，它们各自的位数是按照 逆序 的方式存储的，并且它们的每个节点只能存储 一位 数字。
如果，我们将这两个数相加起来，则会返回一个新的链表来表示它们的和。
您可以假设除了数字 0 之外，这两个数都不会以 0 开头。

>示例：
输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
输出：7 -> 0 -> 8
原因：342 + 465 = 807

``` c++
 ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* head = new ListNode(-1);//存放结果的链表
        ListNode* h = head;//移动指针
        int sum = 0;//每个位的加和结果
        bool carry = false;//进位标志
        while (l1 != NULL || l2 != NULL)
        {
            sum = 0;
            if (l1 != NULL)
            {
                sum += l1->val;
                l1 = l1->next;
            }
            if (l2 != NULL)
            {
                sum += l2->val;
                l2 = l2->next;
            }
            if (carry)
                sum++;
            h->next = new ListNode(sum % 10);
            h = h->next;
            carry = sum >= 10 ? true : false;
        }
        if (carry)
        {
            h->next = new ListNode(1);
        }
        ListNode* ptrDelete = head;
        head = head->next;
        delete ptrDelete;

        return head;
    }
```

## 3.无重复字符的最长子串
 * 3. Longest Substring Without Repeating Characters
   
 来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-substring-without-repeating-characters
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


>给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。

>示例 1:
输入: "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
示例 2:

>输入: "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
示例 3:

>输入: "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

``` c++
int lengthOfLongestSubstring(string s) {
        map<char, int> posMap;
        int ans = 0;
        int start = 0;
        int end = 0;

        while (end < s.length()) {
            char cur = s[end];
            if (posMap.count(cur) > 0) {
                start = max(posMap[cur],start);
            }
            ans = max(end - start + 1, ans);
            posMap[cur] = end + 1;
            end += 1;
        }

        return ans;
    }
```

## 4. 寻找两个正序数组的中位数
* 4. Median of Two Sorted Arrays
  
 来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/median-of-two-sorted-arrays
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定两个大小为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的中位数。
进阶：你能设计一个时间复杂度为 O(log (m+n)) 的算法解决此问题吗？


>示例 1：
输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
解释：合并数组 = [1,2,3] ，中位数 2
示例 2：
输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5
示例 3：
输入：nums1 = [0,0], nums2 = [0,0]
输出：0.00000
示例 4：
输入：nums1 = [], nums2 = [1]
输出：1.00000
示例 5：
输入：nums1 = [2], nums2 = []
输出：2.00000

``` c++
int getKthElement(const vector<int>& nums1, const vector<int>& nums2, int k) {
        int m = nums1.size();
        int n = nums2.size();
        int index1 = 0, index2 = 0;

        while (true) {
            //处理边界
            if (index1 == m)
                return nums2[index2 + k -1];

            if (index2 == n)
                return nums1[index1 + k - 1];

            if (k == 1)
                return min(nums1[index1], nums2[index2]);

            //* 正式处理，查找两个二序列表中第K大的数 *//

            //拿出两个数组 k/2 -1位的数
            int nIndex1 = min(index1 + k / 2 - 1, m-1);
            int nIndex2 = min(index2 + k / 2 - 1,n-1);

            //数组二大！数组一的[0]-[k/2-1]被移去算法范围
            if (nums1[nIndex1] <= nums2[nIndex2]) {
                k -= nIndex1 + 1 - index1;//个数已经比较完，继续剩下的数的比较
                index1 = nIndex1 + 1;
            }
            else{//相关
                k -= nIndex2 + 1 - index2;//个数已经比较完，继续剩下的数的比较
                index2 = nIndex2 + 1;
            }
        }
    }
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int total = nums1.size() + nums2.size();

        if (total % 2 == 1) {
            //奇数个
            return getKthElement(nums1, nums2, (total+1) / 2);
        }
        else {
            //偶数个
            return (getKthElement(nums1, nums2, (total / 2)) + getKthElement(nums1, nums2, total/2 +1)) / 2.0;
        }
    }
```

## 5. 最长回文子串
* 5. Longest Palindromic Substring

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-palindromic-substring
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。
示例 1：
输入: "babad"
输出: "bab"
注意: "aba" 也是一个有效答案。
示例 2：
输入: "cbbd"
输出: "bb"



> 暴力解法：

``` c++
bool validatePalindrome(string s, int i, int j) {
	while (i < j) {
		if (s[i] != s[j]) {
			return false;
		}
		i++;
		j--;
	}
	return true;
}
string QuestionHandler::longestPalindrome(string s) {
	
	if (s == "" || s.length() < 2)
		return s;

	int begin = 0;
	int maxLen = 1;
	for (int i = 0; i < s.length()-1; i++)
	{
		for (int j = i+1; j < s.length(); j++)
		{
			if (((j - i + 1) > maxLen) && validatePalindrome(s, i, j)) {
				maxLen = (j - i + 1);
				begin = i;
			}
		}
	}
	return s.substr(begin, maxLen);
}
```
> 中心扩散法

``` c++
int expandAroundCenter(string s, int left, int right) {
	int len = s.length();
	int i = left;
	int j = right;
	while (i >= 0 && j < len) {
		if (s[i] == s[j]) {
			i--;
			j++;
		}
		else {
			break;
		}
	}
	
	return j - i +1 - 2;
}
string QuestionHandler::longestPalindrome(string s) {
	if (s == "" || s.length() < 2)
		return s;

	int begin = 0;
	int maxLen = 1;
	for (int i = 0; i < s.length() - 1; i++)
	{
		int oddLen = expandAroundCenter(s, i, i);
		int eveLen = expandAroundCenter(s, i, i+1);

		int curMaxLen = max(oddLen, eveLen);
		if (curMaxLen > maxLen) {
			maxLen = curMaxLen;
			begin = i - (curMaxLen - 1) / 2;
		}
	}

	return s.substr(begin, maxLen);

}
```
> 动态规划

``` c++
string QuestionHandler::longestPalindrome(string s) {
	if (s == "" || s.length() < 2)
		return s;

	int len = s.length();
	int begin = 0;
	int maxLen = 1;
	vector<vector<int>> dp(len, vector<int>(len));
	for (int j = 1; j < len; j++) {
		for (int i = 0; i < j; i++) {
			if (s[i] != s[j]) {
				dp[i][j] = 0;
			}
			else {
				if (j - i < 3) {
					dp[i][j] = 1;
				}
				else {
					dp[i][j] = dp[i + 1][j - 1];
				}
			}

			if (dp[i][j] && (j - i + 1) > maxLen) {
				maxLen = j - i + 1;
				begin = i;
			}
		}
	}

	return s.substr(begin, maxLen);
}
```

![动态规划解法](/img/1603943631534.png)

> Manacher算法 - O(n)

``` c++
int expand(const string& s, int left, int right) {
	while (left >= 0 && right < s.size() && s[left] == s[right]) {
		--left;
		++right;
	}
	return (right - left - 2) / 2;
}
string QuestionHandler::longestPalindrome(string s) {
	int start = 0, end = -1;
	string t = "#";
	for (char c : s) {
		t += c;
		t += '#';
	}
	t += '#';
	s = t;

	vector<int> arm_len;
	int right = -1, j = -1;
	for (int i = 0; i < s.size(); ++i) {
		int cur_arm_len;
		if (right >= i) {
			int i_sym = j * 2 - i;
			int min_arm_len = min(arm_len[i_sym], right - i);
			cur_arm_len = expand(s, i - min_arm_len, i + min_arm_len);
		}
		else {
			cur_arm_len = expand(s, i, i);
		}
		arm_len.push_back(cur_arm_len);
		if (i + cur_arm_len > right) {
			j = i;
			right = i + cur_arm_len;
		}
		if (cur_arm_len * 2 + 1 > end - start) {
			start = i - cur_arm_len;
			end = i + cur_arm_len;
		}
	}

	string ans;
	for (int i = start; i <= end; ++i) {
		if (s[i] != '#') {
			ans += s[i];
		}
	}
	return ans;
}
```

## 6.Z 字形变换
* 6. ZigZag Conversion

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zigzag-conversion
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>将一个给定字符串根据给定的行数，以从上往下、从左到右进行 Z 字形排列。
比如输入字符串为 "LEETCODEISHIRING" 行数为 3 时，排列如下：
L   C   I   R
E T O E S I I G
E   D   H   N
之后，你的输出需要从左往右逐行读取，产生出一个新的字符串，比如："LCIRETOESIIGEDHN"。
请你实现这个将字符串进行指定行数变换的函数：
string convert(string s, int numRows);
示例 1:
输入: s = "LEETCODEISHIRING", numRows = 3
输出: "LCIRETOESIIGEDHN"
示例 2:
输入: s = "LEETCODEISHIRING", numRows = 4
输出: "LDREOEIIECIHNTSG"
解释:
L     D     R
E   O E   I I
E C   I H   N
T     S     G

``` c++
  string convert(string s, int numRows) {
        if (numRows == 1) return s;

        int rowIdx = 0;
        vector<string> rowStrs(numRows);
        bool goingDown = false;
        for (char c : s) {
            rowStrs[rowIdx] += c;
            if (rowIdx == 0 || rowIdx == numRows - 1) goingDown = !goingDown;
            rowIdx += goingDown ? 1 : -1;
        }

        string result;
        for (string row : rowStrs) result += row;
        return result;
    }
```

## 7. 整数反转
* 7. Reverse Integer
 
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-integer
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
示例 1:
输入: 123
输出: 321
 示例 2:
输入: -123
输出: -321
示例 3:
输入: 120
输出: 21

``` c++
  int reverse(int x) {
         int ans = 0;
        while (x != 0) {
            if (ans > 214748364 || ans < -214748364) {
                return 0;
            }
            ans = ans*10 + x % 10;
            x /= 10;
        }

        return ans;
    }
```

## 8. 字符串转换整数 (atoi)
* 8. String to Integer (atoi)

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/string-to-integer-atoi
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>请你来实现一个 atoi 函数，使其能将字符串转换成整数。
首先，该函数会根据需要丢弃无用的开头空格字符，直到寻找到第一个非空格的字符为止。接下来的转化规则如下：
如果第一个非空字符为正或者负号时，则将该符号与之后面尽可能多的连续数字字符组合起来，形成一个有符号整数。
假如第一个非空字符是数字，则直接将其与之后连续的数字字符组合起来，形成一个整数。
该字符串在有效的整数部分之后也可能会存在多余的字符，那么这些字符可以被忽略，它们对函数不应该造成影响。
注意：假如该字符串中的第一个非空格字符不是一个有效整数字符、字符串为空或字符串仅包含空白字符时，则你的函数不需要进行转换，即无法进行有效转换。
在任何情况下，若函数不能进行有效的转换时，请返回 0 。
提示：
本题中的空白字符只包括空格字符 ' ' 。
假设我们的环境只能存储 32 位大小的有符号整数，那么其数值范围为 [−231,  231 − 1]。如果数值超过这个范围，请返回  INT_MAX (231 − 1) 或 INT_MIN (−231) 。

>示例 1:
输入: "42"
输出: 42
示例 2:
输入: "   -42"
输出: -42
解释: 第一个非空白字符为 '-', 它是一个负号。
     我们尽可能将负号与后面所有连续出现的数字组合起来，最后得到 -42 。
示例 3:
输入: "4193 with words"
输出: 4193
解释: 转换截止于数字 '3' ，因为它的下一个字符不为数字。
示例 4:
输入: "words and 987"
输出: 0
解释: 第一个非空字符是 'w', 但它不是数字或正、负号。
     因此无法执行有效的转换。
示例 5:
输入: "-91283472332"
输出: -2147483648
解释: 数字 "-91283472332" 超过 32 位有符号整数范围。 
     因此返回 INT_MIN (−231) 。
	 
``` c++
class Automaton {
    string state = "start";
    unordered_map<string, vector<string>> table = {
        {"start", {"start", "signed", "in_number", "end"}},
        {"signed", {"end", "end", "in_number", "end"}},
        {"in_number", {"end", "end", "in_number", "end"}},
        {"end", {"end", "end", "end", "end"}}
    };

    int get_col(char c) {
        if (isspace(c)) return 0;
        if (c == '+' or c == '-') return 1;
        if (isdigit(c)) return 2;
        return 3;
    }
public:
    int sign = 1;
    long long ans = 0;

    void get(char c) {
        state = table[state][get_col(c)];
        if (state == "in_number") {
            ans = ans * 10 + c - '0';
            ans = sign == 1 ? min(ans, (long long)INT_MAX) : min(ans, -(long long)INT_MIN);
        }
        else if (state == "signed")
            sign = c == '+' ? 1 : -1;
    }
};

int myAtoi(string s) {
         Automaton automaton;
        for (char c : s)
            automaton.get(c);
        return automaton.sign * automaton.ans;
    }
```

## 9.回文数
* 9. Palindrome Number
  
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/palindrome-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
示例 1:
输入: 121
输出: true
示例 2:
输入: -121
输出: false
解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。
示例 3:
输入: 10
输出: false
解释: 从右向左读, 为 01 。因此它不是一个回文数。

``` c++
 bool isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }
        //后半段与前半段对比
        int revertedNumber = 0;
        while (x > revertedNumber) {
            revertedNumber = revertedNumber * 10 + x % 10;
            x /= 10;
        }

        return x == revertedNumber || x == revertedNumber / 10;
    }
```

## 10. 正则表达式匹配
* 10. Regular Expression Matching

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/regular-expression-matching
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

给你一个字符串 s 和一个字符规律 p，请你来实现一个支持 '.' 和 '*' 的正则表达式匹配。

> '.' 匹配任意单个字符
'\*' 匹配零个或多个前面的那一个元素
所谓匹配，是要涵盖 整个 字符串 s的，而不是部分字符串。

 
>示例 1：
输入：s = "aa" p = "a"
输出：false
解释："a" 无法匹配 "aa" 整个字符串。

>示例 2:
输入：s = "aa" p = "a*"
输出：true
解释：因为 '\*' 代表可以匹配零个或多个前面的那一个元素, 在这里前面的元素就是 'a'。因此，字符串 "aa" 可被视为 'a' 重复了一次。

>示例 3：
输入：s = "ab" p = ".\*"
输出：true
解释：".\*" 表示可匹配零个或多个（'\*'）任意字符（'.'）。

>示例 4：
输入：s = "aab" p = "c\*a\*b"
输出：true
解释：因为 '\*' 表示零个或多个，这里 'c' 为 0 个, 'a' 被重复一次。因此可以匹配字符串 "aab"。

>示例 5：
输入：s = "mississippi" p = "mis\*is\*p\*."
输出：false

``` c++
bool isMatch(string s, string p) {
	// dp[i][j]表示str[1:i]和pattern[1:j]能否匹配，为0表示无法匹配，为1表示可以匹配
//
// 分析状态转移方程
//   对于dp[i][j]，如果str[i]与p[j]相同或者p[j]为.，则dp[i][j] = dp[i-1][j-1]，即与s[1:i-1]和p[1:j-1]的匹配情况相同
//   如果p[j]为*，则表示这个字符可以联合p[j-1]使用来匹配当前的s[i](这个选择可做可不做，但我们尽量去匹配字符串)
//   考虑p[j]为*，如果p前一个字符为.，显然可以用一次.*组合匹配到s[i]，如果p前一个字符p[j-1]不为.并且不与s[i]相同，则不能使用
//   综合考虑，若p[j]=='*'
//   1. 不选择替换，使用0次*，dp[i][j] = dp[i][j-2]
//   2. 当p[j-1]为.或者与s[i]相同时，可以使用一次替换，则dp[i][j] = dp[i-1][j]
//   两者求或 (因为我们尽可能去匹配字符串，所以只要有一种情况匹配成功，则匹配成功)
// 初始化主要考虑p去匹配一个空串的情况，和上面类似的分析过程即可得出结论

	//dp[i][j] 表示 s 的前 i 个是否能被 p 的前 j 个匹配
	vector<vector<bool>> dp(s.size() + 1, vector<bool>(p.size() + 1));
	dp[0][0] = true;

	//s 的前 0 个是否能被 p 的前 j 个匹配
	for (size_t j = 1; j < p.size(); ++j)
	{
		if (p[j] == '*')
		{
			dp[0][j + 1] = dp[0][j - 1];
		}
	}

	for (size_t i = 0; i < s.size(); ++i)
	{
		for (size_t j = 0; j < p.size(); ++j)
		{
			if (s[i] == p[j] || p[j] == '.')//匹配单个字符  
			{
				dp[i + 1][j + 1] = dp[i][j];
			}
			else if (p[j] == '*' && j > 0)
			{
				if (s[i] != p[j - 1] && p[j - 1] != '.')//前一对字符匹配
				{
					dp[i + 1][j + 1] = dp[i + 1][j - 1];
				}
				else
				{
					dp[i + 1][j + 1] = dp[i][j + 1] || //*表示匹配超过一个字符(s[i]、s[i-1]和p[j-1])
						//dp[i + 1][j] || //*表示只匹配一个字符（s[i]和p[j-1]）
						dp[i + 1][j - 1];//*表示0个匹配
				}

			}
		}
	}

	return dp[s.size()][p.size()];
}
```



## 11. 盛最多水的容器

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/container-with-most-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给你 n 个非负整数 a1，a2，...，an，每个数代表坐标中的一个点 (i, ai) 。在坐标内画 n 条垂直线，垂直线 i 的两个端点分别为 (i, ai) 和 (i, 0)。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。
说明：你不能倾斜容器，且 n 的值至少为 2。

>示例：
输入：[1,8,6,2,5,4,8,3,7]
输出：49

``` c++
int maxArea(vector<int>& height) {
        int n = height.size();
        if (n < 2)
            return 0;

        int maxVolume = 0;
        int left = 0;
        int right = n - 1;
        
        while(left < right){
            //取左端与右端
            int lh = height[left];
            int rh = height[right];

            //计算体积
            int vol = min(lh, rh) * (right-left);
            //设置最大体积
            maxVolume = max(maxVolume, vol);

            //哪端的指针移动，取决于哪根柱子更低
            left += (lh <= rh) ? 1 : 0;
            right -= (lh > rh) ? 1 : 0;

            cout << "left:"<<left<<",right:"<<right<<endl;
        }


        return maxVolume;
    }
```
## 17. 电话号码的字母组合

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。
给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

![17](/img/1604578953107.png)

>示例:
输入："23"
输出：["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
说明:
尽管上面的答案是按字典序排列的，但是你可以任意选择答案输出的顺序。

``` c++
  vector<string> letterCombinations(string digits) {
        map<int,vector<char>> numsMap;
        numsMap.insert(map< int, vector<char>>::value_type(2, vector<char>{'a', 'b', 'c'}));
        numsMap.insert(map< int, vector<char>>::value_type(3, vector<char>{'d', 'e', 'f'}));
        numsMap.insert(map< int, vector<char>>::value_type(4, vector<char>{'g', 'h', 'i'}));
        numsMap.insert(map< int, vector<char>>::value_type(5, vector<char>{'j', 'k', 'l'}));
        numsMap.insert(map< int, vector<char>>::value_type(6, vector<char>{'m', 'n', 'o'}));
        numsMap.insert(map< int, vector<char>>::value_type(7, vector<char>{'p', 'q', 'r','s'}));
        numsMap.insert(map< int, vector<char>>::value_type(8, vector<char>{'t', 'u', 'v'}));
        numsMap.insert(map< int, vector<char>>::value_type(9, vector<char>{'w', 'x', 'y','z'}));

        /*输入："23"
            输出：["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].*/
        map<string, int> resultMap;
        vector<string> result;
        
        for (int i = 0; i < digits.size(); i++) {
            int v = digits[i] - '0';
            if (numsMap.count(v) == 0) {
                result.clear();
                break;
            }
            vector<char> curChars = numsMap[v];
            if (i > 0) {
                vector<string> tmpList;
                for(string val : result) {
                    for (char c : curChars) {
                        tmpList.push_back(val + c);
                    }
                }
                result.clear();
                result = tmpList;
            }
            else {
                for (auto it = curChars.begin(); it != curChars.end(); it++) {
                  	char v = *it;
				    result.push_back(string (1,v));
                }
            }
        }

        return result;
    }
```

## 15.三数之和

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/3sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。
注意：答案中不可以包含重复的三元组。

>示例：
给定数组 nums = [-1, 0, 1, 2, -1, -4]，
满足要求的三元组集合为：
[
  [-1, 0, 1],
  [-1, -1, 2]
]

``` c++
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());   // -4  -1  -1  0  1  2
        vector<vector<int>> res;
        for(int i=0; i<nums.size(); i++){
            if(i > 0 && nums[i] == nums[i-1]){
                continue;
            }
            int j = i+1, k = nums.size() -1;
            while(j < k){
                if(j > i+1 && nums[j] == nums[j-1]){
                    j++;
                    continue;
                }
                if(k < nums.size()-1 && nums[k] == nums[k+1]){
                    k--;
                    continue;
                }
                if(nums[j] + nums[k] > -1*nums[i]){
                    k--;
                }else if(nums[j] + nums[k] < -1*nums[i]){
                    j++;
                }else{
                    res.push_back({nums[i], nums[j], nums[k]});
                    j++, k--;
                }
            }
        }
        return res;
    }
```

## 19.删除链表的倒数第N个节点

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个链表，删除链表的倒数第 n 个节点，并且返回链表的头结点。
示例：
给定一个链表: 1->2->3->4->5, 和 n = 2.
当删除了倒数第二个节点后，链表变为 1->2->3->5.
说明：
给定的 n 保证是有效的。
进阶：
你能尝试使用一趟扫描实现吗？

``` c++
  ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode* slow = head;
        ListNode* fast = head;
        ListNode* pre = NULL;

        for (int i = 0; i < n; i++)
        {
            fast = fast->next;
        }

        while (fast != NULL) {
            pre = slow;
            slow = slow->next;
            fast = fast->next;
        }
        
        if (pre != NULL) {
            pre->next = slow->next;
            return head;
        }
        else {
            return head->next;
        }

    }
	
```

## 20. 有效的括号

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/valid-parentheses
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。
有效字符串需满足：
左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
注意空字符串可被认为是有效字符串。

>示例 1:
输入: "()"
输出: true
示例 2:
输入: "()[]{}"
输出: true
示例 3:
输入: "(]"
输出: false
示例 4:
输入: "([)]"
输出: false
示例 5:
输入: "{[]}"
输出: true

``` c++
 bool isValid(string s) {
        map<char, char> cMap = {
            {']','['},
            {'}','{'},
            {')','('},
        };

        if (s.size() % 2 == 1)//奇数必然不对
            return false;

        stack<char> cs;
        for (char c : s) {
            if (cMap.count(c)) {
                if (cs.empty() || cs.top() != cMap[c]) {
                    return false;
                }
                cs.pop();
            }
            else {
                cs.push(c);
            }
        }
        return cs.size() == 0;
    }
```

## 22. 括号生成

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/generate-parentheses
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

>示例：
输入：n = 3
输出：[
       "((()))",
       "(()())",
       "(())()",
       "()(())",
       "()()()"
     ]


``` c++
 void LoopGetParanthesis(vector<string> & result,string str,int left, int right) {
        if (left == 0 && right == 0) {
            result.push_back(str);
            return;
        }
        
        //左右括号数相等，则只用左括号
        if (left == right) {
            LoopGetParanthesis(result, str + "(", left - 1, right);
        }
        else if(left < right){
            if (left > 0) {
                LoopGetParanthesis(result, str + "(", left-1, right);
            }
            LoopGetParanthesis(result, str + ")", left, right - 1);
        }
    }
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        string str = "";
        LoopGetParanthesis(result, str, n, n);

        return result;
    }
```

## 26.删除排序数组中的重复项
* 26. Remove Duplicates from Sorted Array
 
 来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个排序数组，你需要在 原地 删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。
不要使用额外的数组空间，你必须在 原地 修改输入数组 并在使用 O(1) 额外空间的条件下完成。

>示例 1:
给定数组 nums = [1,1,2], 
函数应该返回新的长度 2, 并且原数组 nums 的前两个元素被修改为 1, 2。 
你不需要考虑数组中超出新长度后面的元素。

>示例 2:
给定 nums = [0,0,1,1,1,2,2,3,3,4],
函数应该返回新的长度 5, 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4。
你不需要考虑数组中超出新长度后面的元素。

``` c++
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        if(nums.size() ==0) return 0;
        int thumb = 0;
        
        for(int i = 1;i < nums.size(); i++){
            if(nums[i] != nums[thumb]){
                thumb ++;
                nums[thumb] = nums[i];
            }
        }
        return thumb+1;
    }
};
```

## 27. 移除元素
* 27. Remove Element

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-element
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。
不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并 原地 修改输入数组。
元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。

>示例 1:
给定 nums = [3,2,2,3], val = 3,
函数应该返回新的长度 2, 并且 nums 中的前两个元素均为 2。
你不需要考虑数组中超出新长度后面的元素。

>示例 2:
给定 nums = [0,1,2,2,3,0,4,2], val = 2,
函数应该返回新的长度 5, 并且 nums 中的前五个元素为 0, 1, 3, 0, 4。
注意这五个元素可为任意顺序。
你不需要考虑数组中超出新长度后面的元素。

``` c++
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int thumb = 0;
        for(int i = 0; i < nums.size(); i++){
            if(nums[i] != val){
                nums[thumb] = nums[i];
                thumb ++;
            }
        }
        return thumb;
    }
};
```

## 28. 实现 strStr()
* 28. Implement strStr()

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/implement-strstr
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>实现 strStr() 函数。
给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。

>示例 1:
输入: haystack = "hello", needle = "ll"
输出: 2

>示例 2:
输入: haystack = "aaaaa", needle = "bba"
输出: -1

``` python
class Solution:
    def strStr(self, source: str, target: str) -> int:
        if source == target:
            return 0

        source_len = len(source)
        target_len = len(target)

        if target_len > source_len:
            return -1

        for i in range(source_len):
            target_index = i + target_len
            if target_index > source_len:
                continue
            if source[i:target_index] == target:
                return i

        return -1
```

## 29. 两数相除
* 29. Divide Two Integers

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/divide-two-integers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。
返回被除数 dividend 除以除数 divisor 得到的商。
整数除法的结果应当截去（truncate）其小数部分，例如：truncate(8.345) = 8 以及 truncate(-2.7335) = -2

 
>示例 1:
输入: dividend = 10, divisor = 3
输出: 3
解释: 10/3 = truncate(3.33333..) = truncate(3) = 3

>示例 2:
输入: dividend = 7, divisor = -3
输出: -2
解释: 7/-3 = truncate(-2.33333..) = -2
 

>提示：
被除数和除数均为 32 位有符号整数。
除数不为 0。
假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−231,  231 − 1]。本题中，如果除法结果溢出，则返回 231 − 1。

``` python
class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        abs_dividend = abs(dividend)
        abs_divisor = abs(divisor)
        if abs_dividend < abs_divisor:
            return 0

        is_neg = 0
        if abs(dividend + divisor) != abs_dividend + abs_divisor:
            is_neg = 1
        ans = 0

        for i in range(31, -1, -1):
            print('abs_dividend >> %d : %d, %d, '% (i, abs_dividend >> i, abs_divisor))

            if abs_dividend >> i >= abs_divisor:
                ans += 1 << i
                abs_dividend -= abs_divisor << i
                print('good value: %d, %d'%(ans, abs_dividend))

        if is_neg and ans >= 2 ** 31:
            return -2 ** 31
        elif ans >= 2 ** 31:
            return 2 ** 31 - 1
        elif is_neg:
            return -ans
        else:
            return ans
```

## 30. 串联所有单词的子串
* 30. Substring with Concatenation of All Words

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/substring-with-concatenation-of-all-words
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个字符串 s 和一些长度相同的单词 words。找出 s 中恰好可以由 words 中所有单词串联形成的子串的起始位置。
注意子串要与 words 中的单词完全匹配，中间不能有其他字符，但不需要考虑 words 中单词串联的顺序。


>示例 1：
输入：
  s = "barfoothefoobarman",
  words = ["foo","bar"]
输出：[0,9]
解释：
从索引 0 和 9 开始的子串分别是 "barfoo" 和 "foobar" 。
输出的顺序不重要, [9,0] 也是有效答案。

>示例 2：
输入：
  s = "wordgoodgoodgoodbestword",
  words = ["word","good","best","word"]
输出：[]

``` python
class Solution(object):
    def findSubstring(self, s, words):
        from collections import Counter
        if not s or not words:return []
        one_word = len(words[0])
        all_len = len(words) * one_word
        n = len(s)
        words = Counter(words)
        res = []
        for i in range(0, n - all_len + 1):
            tmp = s[i:i+all_len]
            c_tmp = []
            for j in range(0, all_len, one_word):
                c_tmp.append(tmp[j:j+one_word])
            if Counter(c_tmp) == words:
                res.append(i)
        return res
```


## 41. 缺失的第一个正数
* 41. First Missing Positive
 
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/first-missing-positive
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给你一个未排序的整数数组，请你找出其中没有出现的最小的正整数。

>示例 1:
输入: [1,2,0]
输出: 3

>示例 2:
输入: [3,4,-1,1]
输出: 2

>示例 3:
输入: [7,8,9,11,12]
输出: 1
 

>提示：
你的算法的时间复杂度应为O(n)，并且只能使用常数级别的额外空间。

``` c++
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
         // 总长
        int n = nums.size();
        // 1. 全部元素没有1，返回1
        bool noOne = true;
        for(int i = 0; i < nums.size();i++){
            if(nums[i] == 1)
            {
                noOne = false;
                break;
            }
        }
        if(noOne){
            return 1;
        }

        //2. 只有一个元素，且为[1]，则返回2
        if(n == 1)
        {
            return 2;
        }

        //3. 去<= 0与 > 总数的数，将其设为1
        for(int i = 0; i < n;i++){
            if(i == n-1){
                cout << nums[i] << endl;
            }
            if(nums[i] < 1 || nums[i] > n){
                nums[i] = 1;
            }
        }
  

        //4.遍历，当值 == 总数。第一个值设为负数. 当值 <= 总数，以值为下标设置为负值. 特别的，当值为总数时，将第一个值为负值！
         for(int i = 0; i < n; i++){
             int a = abs(nums[i]);
             if(a == n){
                 nums[0] = - abs(nums[0]);
             }else{
                nums[a] = - abs(nums[a]);
             }
         }

        for(int v: nums){
            cout << v << ",";
        }
        cout << endl;

        //5.遍历最新的数组中，发现有大于0，此索引就是丢失的最小正数
        for(int i = 1; i < n;i++){
            if(nums[i] > 0){
                return i;
            }
        }

        //6.5如果没有找到，第一值取出来如果是正数，则数为正数N
        if(nums[0] > 0){
            return n;
        }

        //7.如果以上走完了，返回n+1
        return n+1;
    }
};
```

## 42. 接雨水

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/trapping-rain-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
示例 1：

![接雨水](/img/1604063667003.png)

>输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。 
示例 2：
输入：height = [4,2,0,3,2,5]
输出：9

``` c++
  int trap(vector<int>& height) {
        int left = 0, right = height.size() - 1;
        int ans = 0;
        int left_max = 0, right_max = 0;
        while (left < right) {
            //情况1：左比右低，只有当左边最高柱比当前柱要高，则这个落差必定是能装水的。
            if (height[left] < height[right]) {
                height[left] >= left_max ? (left_max = height[left]) : ans += (left_max - height[left]);
                ++left;
            }
            else {//情况2：右比左低，只有当右边最高柱比当前柱要高，则这个落差必定是能装水的。
                height[right] >= right_max ? (right_max = height[right]) : ans += (right_max - height[right]);
                --right;
            }
        }
        return ans;
    }
```
## 51. N皇后 & 52. N皇后 II
* 51. N-Queens
* 52. N-Queens II
 
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/n-queens
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。

![8皇后的一种解法](/img/1601178139148.png)

>51. 给定一个整数 n，返回所有不同的 n 皇后问题的解决方案。
每一种解法包含一个明确的 n 皇后问题的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。
>52. 给定一个整数 n，返回 n 皇后不同的解决方案的数量。


``` python
class NQueen:
    def __init__(self):
        self.count = 0

    def do_nqueen(self, n):
        empty_sign = "[O]"
        queen_sign = "[1]"
        # 所有数组起点都以0开始

        # 1.定义所有解的容器，二维数组，第二维代表一个完整的解
        ans = []

        # 2.递归函数dfs
        def dfs(nums, row):
            # 如果找的行数与n相等了，说明已经找完了，得到一个解！
            if row == n:
                ans.append(nums[:]) # 注意不可用ans.append(nums)
                return
            # 逐列进行尝试，列的总数为n
            for i in range(n):
                # 每进行到一列，标记当前行皇后位置为此列
                nums[row] = i
                # 往下递归找到，一直找到底，找不到底循环会返回到此处！
                if valid(nums, row):
                    # print("当前找到第%d行的第%d列，此值可放皇后！"%(row, i))
                    dfs(nums, row+1)
                else:
                    pass
                    # print("当前找到第%d行的第%d列，不可放，回溯"%(row, i))

        # 3.检查函数valid
        def valid(nums, row):
            # 只找前面行的点， 皇后攻击规则，同列同行 和 对角线元素表示
            for r in range(row):
                if abs(nums[r] - nums[row]) == abs(r - row) or nums[r] == nums[row]:
                    return False
            return True

        # 4.执行, 从第0行开始找n数组长度中的位置
        dfs([None for _ in range(n)], 0)

        def get_row_list(row_val, count):
            result = []
            for i in range(count):
                if i == row_val:
                    result.append(queen_sign)
                else:
                    result.append(empty_sign)
            return result


        # 5.结果画出来
        result = [[] for _ in range(len(ans))]
        for i in range(len(ans)):
            for col in ans[i]:
                result[i].append("".join(get_row_list(col, n)))

        return result


myqueen = NQueen()
result = myqueen.do_nqueen(4)
print("解有%d个"%len(result))
for r in result:
    r = str(r)
    print(r+"\n\n")
```

## 75. 颜色分类

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sort-colors
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个包含红色、白色和蓝色，一共 n 个元素的数组，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。
此题中，我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。
注意:
不能使用代码库中的排序函数来解决这道题。
示例:
输入: [2,0,2,1,1,0]
输出: [0,0,1,1,2,2]
进阶：
一个直观的解决方案是使用计数排序的两趟扫描算法。
首先，迭代计算出0、1 和 2 元素的个数，然后按照0、1、2的排序，重写当前数组。
你能想出一个仅使用常数空间的一趟扫描算法吗？

``` c++
 void sortColors(vector<int>& nums) {
       int n = nums.size();
        int slow0 = 0, fast = 0, slow2 = n - 1;

        while (fast <= slow2) {
            while (fast <= slow2 && nums[fast] == 2) {
                //当当前快指针为2时，移至结尾。如果换完后的nums[fast]还是2？则继续换
                nums[fast] = nums[slow2];
                nums[slow2--] = 2;
            }
            
            if (nums[fast] == 0) {
                nums[fast] = nums[slow0];
                nums[slow0++] = 0;
            }
            fast++;
        }
    }
```

## 76.最小覆盖子串

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-window-substring
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给你一个字符串 S、一个字符串 T 。请你设计一种算法，可以在 O(n) 的时间复杂度内，从字符串 S 里面找出：包含 T 所有字符的最小子串。
示例：
输入：S = "ADOBECODEBANC", T = "ABC"
输出："BANC"

>提示：
如果 S 中不存这样的子串，则返回空字符串 ""。
如果 S 中存在这样的子串，我们保证它是唯一的答案。

```c++
 string minWindow(string s, string t) {
        if(s == t) return s;

        map<char, int> need, window;
        int tLen = t.length();//目标字符串
        int sLen = s.length();
        if (tLen == 0 || sLen == 0) return "";
        if (sLen < tLen )
            return "";

        //先把t中的字符放到need表中，计数
        for (int i = 0; i < tLen; i++) {
            char c = t[i];
            need[c] = ((need.count(c) == 0)?0:need[c]) + 1;
        }

        int left = 0, right = 0;
        int len = INT32_MAX, start = 0;
        int valid = 0; //已经匹配成功的字符种类数（非字符个数）

        //当右指针去到字符串末尾前
        while (right < sLen) {
            char c = s[right];
            right++;//右指针向右滑

            //如果右指针现在滑到的字符是目标字符串的一个，那么更新窗口中的数据
            if (need.count(c) > 0) {
                window[c] = ((window.count(c) == 0)?0:window[c]) + 1;
                if (window[c] == (need[c])) {
                    valid++;
                }
            }

            //窗口开始从左边收缩
            while (valid == need.size()) {
                if (right - left < len) {
                    start = left;
                    len = right - left;
                }
                
                char d = s[left];
                left++;

                if (need.count(d) > 0) {
                    if (window[d] == (need[d])) {
                        valid--;
                    }
                    window[d] = window[d] - 1;
                }
            }
        }
        return len == INT32_MAX ? "" : s.substr(start, len);
    }
```

## 80. 删除排序数组中的重复项 II
* 80. Remove Duplicates from Sorted Array II

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素最多出现两次，返回移除后数组的新长度。
不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。

>示例 1:
给定 nums = [1,1,1,2,2,3],
函数应返回新长度 length = 5, 并且原数组的前五个元素被修改为 1, 1, 2, 2, 3 。
你不需要考虑数组中超出新长度后面的元素。

>示例 2:
给定 nums = [0,0,1,1,1,1,2,3,3],
函数应返回新长度 length = 7, 并且原数组的前五个元素被修改为 0, 0, 1, 1, 2, 3, 3 。
你不需要考虑数组中超出新长度后面的元素。

>说明:
为什么返回数值是整数，但输出的答案是数组呢?

``` c++
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
      int i = 0;
        for (int n : nums) {
            if (i < 2 || n > nums[i-2]) nums[i++] = n;
        }
        return i;
    }
};
```

## 127. 单词接龙

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/word-ladder
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定两个单词（beginWord 和 endWord）和一个字典，找到从 beginWord 到 endWord 的最短转换序列的长度。转换需遵循如下规则：
每次转换只能改变一个字母。
转换过程中的中间单词必须是字典中的单词。

 >说明:
如果不存在这样的转换序列，返回 0。
所有单词具有相同的长度。
所有单词只由小写字母组成。
字典中不存在重复的单词。
你可以假设 beginWord 和 endWord 是非空的，且二者不相同。

>示例 1:
输入:
beginWord = "hit",
endWord = "cog",
wordList = ["hot","dot","dog","lot","log","cog"]
输出: 5
解释: 一个最短转换序列是 "hit" -> "hot" -> "dot" -> "dog" -> "cog",
     返回它的长度 5。
示例 2:
输入:
beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","lot","log"]
输出: 0
解释: endWord "cog" 不在字典中，所以无法进行转换。

``` c++
class Solution {
    unordered_map<string, int> wordId;
    vector<vector<int>> edge;
    int nodeNum = 0;

    void addWord(string& word) {
        if (!wordId.count(word)) {
            wordId[word] = nodeNum++;
            edge.emplace_back();
        }
    }

    void addEdge(string& word) {
        addWord(word);
        int id1 = wordId[word];
        for (char& it : word) {
            char tmp = it;
            it = '*';
            addWord(word);
            int id2 = wordId[word];
            edge[id1].push_back(id2);
            edge[id2].push_back(id1);
            it = tmp;
        }
    }
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        for (string& word : wordList) {
            addEdge(word);
        }
        addEdge(beginWord);
        if (!wordId.count(endWord)) {
            return 0;
        }
        vector<int> dis(nodeNum, INT_MAX);
        int beginId = wordId[beginWord], endId = wordId[endWord];
        dis[beginId] = 0;

        queue<int> que;
        que.push(beginId);
        while (!que.empty()) {
            int x = que.front();
            que.pop();
            if (x == endId) {
                return dis[endId] / 2 + 1;
            }
            for (int& it : edge[x]) {
                if (dis[it] == INT_MAX) {
                    dis[it] = dis[x] + 1;
                    que.push(it);
                }
            }
        }
        return 0;
    }

};
```

## 129.求根到叶子节点数字之和
* 129. Sum Root to Leaf Numbers
* 
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sum-root-to-leaf-numbers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个二叉树，它的每个结点都存放一个 0-9 的数字，每条从根到叶子节点的路径都代表一个数字。
例如，从根到叶子节点路径 1->2->3 代表数字 123。
计算从根到叶子节点生成的所有数字之和。
说明: 叶子节点是指没有子节点的节点。

示例 1:
输入: [1,2,3]
    1
   / \
  2   3
输出: 25
解释:
从根到叶子节点路径 1->2 代表数字 12.
从根到叶子节点路径 1->3 代表数字 13.
因此，数字总和 = 12 + 13 = 25.
示例 2:

输入: [4,9,0,5,1]
    4
   / \
  9   0
 / \
5   1
输出: 1026
解释:
从根到叶子节点路径 4->9->5 代表数字 495.
从根到叶子节点路径 4->9->1 代表数字 491.
从根到叶子节点路径 4->0 代表数字 40.
因此，数字总和 = 495 + 491 + 40 = 1026.

``` c++
int bfs_sum(TreeNode* root) {
	if(root == NULL)
		return 0;
	int sum = 0;
	queue<TreeNode*> q;
	queue<int> qn;

	q.push(root);
	qn.push(root->val);

	while (!q.empty()) {
		TreeNode* node = q.front();
		int nodeVal = qn.front();
		q.pop();
		qn.pop();

		if ((node->left == NULL) && (node->right == NULL)) {
			sum += nodeVal;
		}
		else {
			if (node->left != NULL) {
				q.push(node->left);
				qn.push(nodeVal * 10 + node->left->val);
			}
			if (node->right != NULL) {
				q.push(node->right);
				qn.push(nodeVal * 10 + node->right->val);
			}
		}
	}
	return sum;
}

int dfs_sum(TreeNode* node, int prevSum) {
	if(node == NULL)
		return 0;

	int sum = prevSum * 10 + node->val;
	//左右都没有值 
	if ((node->left == NULL) &&(node->right == NULL)) {
		return sum;
	}
	else {
		sum = dfs_sum(node->left, sum) + dfs_sum(node->right, sum);
	}

	return sum;
}

int sumNumbers(TreeNode* root) {
		//return dfs_sum(root, 0);
	return bfs_sum(root);
}
```
## 141. 环形链表

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/linked-list-cycle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个链表，判断链表中是否有环。
如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。 为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。注意：pos 不作为参数进行传递，仅仅是为了标识链表的实际情况。
如果链表中存在环，则返回 true 。 否则，返回 false 。


>进阶
你能用 O(1)（即，常量）内存解决此问题吗？

>输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。

``` c++
    bool hasCycle(ListNode *head) {
        if(head == NULL)
            return false;
       ListNode* slow = head;
        ListNode* fast = head->next;
        while (slow != fast) {
            if (fast == NULL || fast->next == NULL)
            {
                return false;
            }
                
            slow = slow->next;
            fast = fast->next->next;
        }
        return true;
    }
```

## 142. 环形链表 II
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/linked-list-cycle-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。
为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。注意，pos 仅仅是用于标识环的情况，并不会作为参数传递到函数中。

>输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。

``` c++
    ListNode *detectCycle(ListNode *head) {
        ListNode *slow = head;
        ListNode *fast = head;
        while(fast != NULL){
            if(fast->next == NULL)
                return nullptr;

            slow = slow->next;
            fast = fast->next->next;

            if(slow == fast){
                ListNode * ptr = head;
                while(ptr != slow){
                    ptr = ptr->next;
                    slow = slow->next;
                }
                return ptr;
            }
        }
        return nullptr;

    }
```

## 144. 二叉树的前序遍历
* 144. Binary Tree Preorder Traversal
  
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-tree-preorder-traversal
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个二叉树，返回它的 前序 遍历。

>示例:
输入: [1,null,2,3]  
   1
    \
     2
    /
   3 
输出: [1,2,3]

``` c++
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> result;
        if(root == NULL)
            return result;
        
        stack<TreeNode> ss;
        ss.push(*root);
        
        while(!ss.empty()){
            TreeNode cur = ss.top();
            ss.pop();

            result.push_back(cur.val);

            if(cur.right != NULL){
                ss.push(*cur.right);
            }
            if(cur.left != NULL){
                ss.push(*cur.left);
            }
        }
        return result;
    }
```

## 189. 旋转数组
* 189. Rotate Array

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/rotate-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个数组，将数组中的元素向右移动 k 个位置，其中 k 是非负数。

>示例 1:
输入: [1,2,3,4,5,6,7] 和 k = 3
输出: [5,6,7,1,2,3,4]
解释:
向右旋转 1 步: [7,1,2,3,4,5,6]
向右旋转 2 步: [6,7,1,2,3,4,5]
向右旋转 3 步: [5,6,7,1,2,3,4]

>示例 2:
输入: [-1,-100,3,99] 和 k = 2
输出: [3,99,-1,-100]
解释: 
向右旋转 1 步: [99,-1,-100,3]
向右旋转 2 步: [3,99,-1,-100]

>说明:
尽可能想出更多的解决方案，至少有三种不同的方法可以解决这个问题。
要求使用空间复杂度为 O(1) 的 原地 算法。

``` c++
class Solution {
public:
    void reverse(vector<int>& nums, int start, int end){
        for(int i = start,j = end; i < j; i++,j--){
            int ftmp = nums[j];
            nums[j] = nums[i];
            nums[i] = ftmp;
        }
    }

    void rotate(vector<int>& nums, int k) {
        if(k > nums.size()){
            k %= nums.size();
        }
        
        reverse(nums, 0, nums.size()-k-1);
        reverse(nums, nums.size()-k, nums.size()-1);
        reverse(nums, 0, nums.size()-1);
    }
};

```

## 234. 回文链表

 来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/palindrome-linked-list/
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>请判断一个链表是否为回文链表。
示例 1:
输入: 1->2
输出: false
示例 2:
输入: 1->2->2->1
输出: true

``` c++
ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;
        while (curr != nullptr) {
            ListNode* nextTemp = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
    }

    ListNode* endOfFirstHalf(ListNode* head) {
        ListNode* fast = head;
        ListNode* slow = head;
        while (fast->next != nullptr && fast->next->next != nullptr) {
            fast = fast->next->next;
            slow = slow->next;
        }
        return slow;
    }
    bool isPalindrome(ListNode* head) {
        if(head == NULL)
            return true;
        // 找到前半部分链表的尾节点并反转后半部分链表
        ListNode* firstHalfEnd = endOfFirstHalf(head);
        ListNode* secondHalfStart = reverseList(firstHalfEnd->next);

        // 判断是否回文
        ListNode* p1 = head;
        ListNode* p2 = secondHalfStart;
        bool result = true;
        while (result && p2 != nullptr) {
            if (p1->val != p2->val) {
                result = false;
            }
            p1 = p1->next;
            p2 = p2->next;
        }

        // 还原链表并返回结果
        firstHalfEnd->next = reverseList(secondHalfStart);
        return result;
    }
```

## 283. 移动零

 来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/move-zeroes/
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
输入: [0,1,0,3,12]
输出: [1,3,12,0,0]

``` c++
 void moveZeroes(vector<int>& nums) {
       for (int lastNonZeroFoundAt = 0, cur = 0; cur < nums.size(); cur++) {
            if (nums[cur] != 0) {
                swap(nums[lastNonZeroFoundAt], nums[cur]);
                lastNonZeroFoundAt++;
            }
        }
    }
```

## 287. 寻找重复数

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-the-duplicate-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个包含 n + 1 个整数的数组 nums，其数字都在 1 到 n 之间（包括 1 和 n），可知至少存在一个重复的整数。假设只有一个重复的整数，找出这个重复的数。
示例 1:
输入: [1,3,4,2,2]
输出: 2
示例 2:
输入: [3,1,3,4,2]
输出: 3
说明：

>不能更改原数组（假设数组是只读的）。
只能使用额外的 O(1) 的空间。
时间复杂度小于 O(n2) 。
数组中只有一个重复的数字，但它可能不止重复出现一次。

``` c++
 int findDuplicate(vector<int>& nums) {
        int slow = 0, fast = 0;
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
```

## 299. 猜数字游戏
* 299. Bulls and Cows

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/bulls-and-cows
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>你在和朋友一起玩 猜数字（Bulls and Cows）游戏，该游戏规则如下：
你写出一个秘密数字，并请朋友猜这个数字是多少。
朋友每猜测一次，你就会给他一个提示，告诉他的猜测数字中有多少位属于数字和确切位置都猜对了（称为“Bulls”, 公牛），有多少位属于数字猜对了但是位置不对（称为“Cows”, 奶牛）。
朋友根据提示继续猜，直到猜出秘密数字。
请写出一个根据秘密数字和朋友的猜测数返回提示的函数，返回字符串的格式为 xAyB ，x 和 y 都是数字，A 表示公牛，用 B 表示奶牛。

>xA 表示有 x 位数字出现在秘密数字中，且位置都与秘密数字一致。
>yB 表示有 y 位数字出现在秘密数字中，但位置与秘密数字不一致。
请注意秘密数字和朋友的猜测数都可能含有重复数字，每位数字只能统计一次。

 

>示例 1:
输入: secret = "1807", guess = "7810"
输出: "1A3B"
解释: 1 公牛和 3 奶牛。公牛是 8，奶牛是 0, 1 和 7。

>示例 2:
输入: secret = "1123", guess = "0111"
输出: "1A1B"
解释: 朋友猜测数中的第一个 1 是公牛，第二个或第三个 1 可被视为奶牛。

>说明: 你可以假设秘密数字和朋友的猜测数都只包含数字，并且它们的长度永远相等

``` c++
class Solution {
public:
    string getHint(string secret, string guess) {
        int bulls = 0;
        int cows = 0;
        int ds[10]{0};
        int dg[10]{0};
        for(int i = 0; i < secret.size(); i++){
            int x = secret[i] - '0';
            int y = guess[i] - '0';
            if(secret[i] == guess[i]){
                bulls ++;    
            }
            ds[x] ++;
            dg[y] ++;
        }

        //算出相同元素总数，当然减掉之前算好的cows
        for(int i = 0;i < 10;i++){
            cows += min(ds[i],dg[i]);
        }
        cows -= bulls;
        ostringstream oss;
        oss << bulls << "A" << cows << "B" ;
        return oss.str();
    }

};  
```

## 463. 岛屿的周长

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/island-perimeter
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给定一个包含 0 和 1 的二维网格地图，其中 1 表示陆地 0 表示水域。
网格中的格子水平和垂直方向相连（对角线方向不相连）。整个网格被水完全包围，但其中恰好有一个岛屿（或者说，一个或多个表示陆地的格子相连组成的岛屿）。
岛屿中没有“湖”（“湖” 指水域在岛屿内部且不和岛屿周围的水相连）。格子是边长为 1 的正方形。网格为长方形，且宽度和高度均不超过 100 。计算这个岛屿的周长。

>示例 :
输入:
[[0,1,0,0],
 [1,1,1,0],
 [0,1,0,0],
 [1,1,0,0]]
输出: 16

``` c++
class Solution {
    constexpr static int dx[4] = {0, 1, 0, -1};
    constexpr static int dy[4] = {1, 0, -1, 0};
public:
    int islandPerimeter(vector<vector<int>>& grid) {
        int n = grid.size(), m = grid[0].size();
        int ans = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                if (grid[i][j]) {
                    int cnt = 0;
                    for (int k = 0; k < 4; ++k) {
                        int tx = i + dx[k];
                        int ty = j + dy[k];
                        if (tx < 0 || tx >= n || ty < 0 || ty >= m || !grid[tx][ty]) {
                            cnt += 1;
                        }
                    }
                    ans += cnt;
                }
            }
        }
        return ans;
    }
};
```




## 1207.独一无二的出现次数
* 1207. Unique Number of Occurrences

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/unique-number-of-occurrences
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

>给你一个整数数组 arr，请你帮忙统计数组中每个数的出现次数。
如果每个数的出现次数都是独一无二的，就返回 true；否则返回 false。

>示例 1：
输入：arr = [1,2,2,1,1,3]
输出：true
解释：在该数组中，1 出现了 3 次，2 出现了 2 次，3 只出现了 1 次。没有两个数的出现次数相同。
示例 2：
输入：arr = [1,2]
输出：false
示例 3：
输入：arr = [-3,0,1,-3,1,1,1,-3,10,0]
输出：true

``` c++
bool uniqueOccurrences(vector<int>& arr) {
	map<int, int> posMap;
	for (int i = 0; i < arr.size(); i++)
	{
		posMap[arr[i]] += 1;
	}

	set<int> uniqueSet;
	for (const auto& item : posMap)
	{
		uniqueSet.insert(item.second);
	}

	return posMap.size() == uniqueSet.size();
}
```


