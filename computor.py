import argparse
import sys

def parsing():
    parser = argparse.ArgumentParser(description='ComputorV1')
    parser.add_argument('equation', type=str, help='Equation to solve')
    args = parser.parse_args()
    return args

def update_left_right(side, split_value, next_value):
    try:
        side = side.split(split_value)[1]
    except:
        pass

    if next_value in side or next_value == "":
            next = True
    else:
        next = False

    return side.strip(), next

def to_int_if_possible(value):
    return int(value) if isinstance(value, float) and value.is_integer() else value

def simplify(equation):
    translation_table = str.maketrans('', '', " *-+")
    left = equation.split('=')[0]
    right = equation.split('=')[1]
    sign = ""
    
    sign = left.split('X^0')[0][0] if left.split('X^0')[0][0] == "-" else ""
    c_left = float(left.split('X^0')[0].translate(translation_table))
    c_left = c_left * -1 if sign == "-" else c_left
    left, next = update_left_right(left, 'X^0', 'X^1')

    sign = (left.split('X^1')[0][0])
    b_left = float(left.split('X^1')[0].translate(translation_table) if next == True else '0')
    b_left = b_left * -1 if sign == "-" else b_left
    left, next = update_left_right(left, 'X^1', 'X^2')

    try:
        sign = (left.split('X^2')[0][0])
        a_left = float(left.split('X^2')[0].translate(translation_table) if next == True else '0')
        a_left = a_left * -1 if sign == "-" else a_left
        left, next = update_left_right(left, 'X^2', "")
    except:
        a_left = 0
        sign = ""

    sign = (right.split('X^0')[0].strip()[0]) if right.split('X^0')[0].strip()[0] == "-" else ""
    c_right = float(right.split('X^0')[0].translate(translation_table))
    c_right = c_right * -1 if sign == "-" else c_right
    right, next = update_left_right(right, 'X^0', 'X^1')

    try:
        sign (right.split('X^1')[0][0])
        b_right = float(right.split('X^1')[0].translate(translation_table) if next == True else '0')
        b_right = b_right * -1 if sign == "-" else b_right
        right, next = update_left_right(right, 'X^1', 'X^2')
    except:
        b_right = 0
        sign = ""

    try:
        sign = (right.split('X^2')[0][0])
        a_right = float(right.split('X^2')[0].translate(translation_table) if next == True else '0')
        a_right = a_right * -1 if sign == "-" else a_right
        right, next = update_left_right(right, 'X^2', "")
    except:
        a_right = 0

    # print(a_left, b_left, c_left, a_right, b_right, c_right)

    a = to_int_if_possible(a_left - a_right)
    b = to_int_if_possible(b_left - b_right)
    c = to_int_if_possible(c_left - c_right)

    translation_table = str.maketrans('+-', '-+')
    right = right.translate(translation_table)

    # right = right + " " if right != "" else right.strip()
    # left = left + " " if left != "" else left.strip()
    degree = more_than_2(left, right)
    print("Reduced form:", c, "* X^0" + formate(b, degree, 1) + formate(a, degree, 2) + left + right + " = 0")

    return a, b, c, degree

def formate(value, max_degree, degree):
    string = ""
    if value < 0:
        string = " - " + str(value * -1) + " * X^" + str(degree)
    else:
        string = " + " + str(value) + " * X^" + str(degree)
    if value == 0 and degree == max_degree:
        string = ""
    if degree == 2 and max_degree > 2:
        string = string + " "
    return string

def more_than_2(left, right):
    degree = 2
    for l in left:
        if l == 'X' and left[left.index(l) + 1] == '^':
            degree = int(left[left.index(l) + 2]) if int(left[left.index(l) + 2]) > degree else degree
    for l in right:
        if l == 'X' and right[right.index(l) + 1] == '^':
            degree = int(right[right.index(l) + 2]) if int(right[right.index(l) + 2]) > degree else degree
    return degree
    

def compute_delta(a, b, c):
    # print(a,b,c)
    delta = (b ** 2) - (4 * a * c)
    if delta > 0:
        print("Discriminant is strictly positive, the two solutions are:")
        print("X1 =", (-b + delta ** 0.5) / (2 * a))
        print("X2 =", (-b - delta ** 0.5) / (2 * a))
    elif delta < 0:
        print("Discriminant is strictly negative, the two solutions (in ℂ) are:")
        print("Z1 = (", -b ,"- i *",  (-delta) ** 0.5, ") /", (2 * a))
        print("Z1 = (", -b ,"+ i *",  (-delta) ** 0.5, ") /", (2 * a))
        # print("Z1 = (", -b / (2 * a) ,") - ( i * ",  (-delta) ** 0.5 / (2 * a), ")")
        # print("Z2 = (", -b / (2 * a) ,") + ( i * ",  (-delta) ** 0.5 / (2 * a), ")")

    else :
        print("Discriminant is null, the solution is:")
        print("X =", -b / (2 * a))
    return delta

def main():
    if (len(sys.argv) != 2):
        print('Usage: python3 computor.py "equation"')
        sys.exit(1)
    args = parsing()
    a, b, c, degree = simplify(args.equation)
    if degree > 2 :
        print("Polynomial degree:", degree)
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        sys.exit(1)
    if a == 0 and b == 0:
        print("Polynomial degree: 0")
        print("The solution is:")
        print("All real numbers are solutions")
        exit(0)
    if a == 0:
        print("Polynomial degree: 1")
        print("The solution is:")
        print("X =", -c / b)
        exit(0)
    print("Polynomial degree:", degree)
    compute_delta(a, b, c)

if __name__ == '__main__':
    main()