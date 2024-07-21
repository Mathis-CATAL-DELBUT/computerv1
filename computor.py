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
    
def simplify(equation):
    translation_table = str.maketrans('', '', " *-+")
    left = equation.split('=')[0]
    right = equation.split('=')[1]
    sign = []
    
    c_left = float(left.split('X^0')[0].translate(translation_table))
    left, next = update_left_right(left, 'X^0', 'X^1')

    sign.append(left.split('X^1')[0][0])
    b_left = float(left.split('X^1')[0].translate(translation_table) if next == True else '0')
    left, next = update_left_right(left, 'X^1', 'X^2')

    sign.append(left.split('X^2')[0][0])
    a_left = float(left.split('X^2')[0].translate(translation_table) if next == True else '0')
    left, next = update_left_right(left, 'X^2', "")

    c_right = float(right.split('X^0')[0].translate(translation_table))
    right, next = update_left_right(right, 'X^0', 'X^1')

    b_right = float(right.split('X^1')[0].translate(translation_table) if next == True else '0')
    right, next = update_left_right(right, 'X^1', 'X^2')

    a_right = float(right.split('X^2')[0].translate(translation_table) if next == True else '0')
    right, next = update_left_right(right, 'X^2', "")

    a = int(a_left - a_right) if (a_left - a_right).is_integer() else a_left - a_right
    b = int(b_left - b_right) if (b_left - b_right).is_integer() else b_left - b_right
    c = int(c_left - c_right) if (c_left - c_right).is_integer() else c_left - c_right

    translation_table = str.maketrans('+-', '-+')
    right = right.translate(translation_table)

    right = right + " " if right != "" else right
    left = left + " " if left != "" else left
    print("Reduced form:", c, "* X^0", sign[0], b , "* X^1", sign[1], a , "* X^2 " + left + right + "= 0")

    return a, b, c, left, right

def more_than_2(left, right):
    degree = 0
    for l in left:
        if l == 'X' and left[left.index(l) + 1] == '^':
            degree = int(left[left.index(l) + 2]) if int(left[left.index(l) + 2]) > degree else degree
    for l in right:
        if l == 'X' and right[right.index(l) + 1] == '^':
            degree = int(right[right.index(l) + 2]) if int(right[right.index(l) + 2]) > degree else degree
    print("Polynomial degree:", degree)
    print("The polynomial degree is strictly greater than 2, I can't solve.")
    sys.exit(1)

def compute_delta(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        print("Discriminant is strictly positive, the two solutions are:")
        print("X1 =", (-b + delta ** 0.5) / (2 * a))
        print("X2 =", (-b - delta ** 0.5) / (2 * a))
    elif delta < 0:
        print("Discriminant is strictly negative, the two solutions (in ℂ) are:")
        print("Z1 = (", -b / (2 * a) ,") - ( i * ",  (-delta) ** 0.5 / (2 * a), ")")
        print("Z2 = (", -b / (2 * a) ,") + ( i * ",  (-delta) ** 0.5 / (2 * a), ")")

    else :
        print("Discriminant is null, the solution is:")
        print("X =", -b / (2 * a))
    return delta

def main():
    if (len(sys.argv) != 2):
        print('Usage: python3 computor.py "equation"')
        sys.exit(1)
    args = parsing()
    a, b, c, left, right = simplify(args.equation)
    if left != "" or (right != "" and right.strip() != "0"):
        more_than_2(left, right)
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
    compute_delta(a, b, c)

if __name__ == '__main__':
    main()