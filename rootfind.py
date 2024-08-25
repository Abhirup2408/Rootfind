import streamlit as st
import math

# Root-finding methods
def bisection_method(func, a, b, tol=1e-6, max_iter=100):
    if func(a) * func(b) > 0:
        raise ValueError("The function values at the interval endpoints must have opposite signs.")
    iteration = 0 
    while (b - a) / 2 > tol and iteration < max_iter:
        c = (a + b) / 2  # Compute the midpoint
        if func(c) == 0:
            return c  # Found exact root
        elif func(c) * func(a) < 0:
            b = c  # Root lies in the left subinterval [a, c]
        else:
            a = c  # Root lies in the right subinterval [c, b]
        iteration += 1 
    return (a + b) / 2 

def newton_raphson_method(func, func_derivative, initial_guess, tol=1e-6, max_iter=100):
    x = initial_guess
    iteration = 0  
    while abs(func(x)) > tol and iteration < max_iter:
        x = x - func(x) / func_derivative(x)  
        iteration += 1  
    return x 

def secant_method(func, x0, x1, tol=1e-6, max_iter=100):
    x_k_minus_1 = x0
    x_k = x1

    for k in range(max_iter):
        f_k_minus_1 = func(x_k_minus_1)
        f_k = func(x_k)
        x_k_plus_1 = x_k - f_k * (x_k - x_k_minus_1) / (f_k - f_k_minus_1)
        if abs(x_k_plus_1 - x_k) < tol:
            return x_k_plus_1, k + 1  # Return the root and the number of iterations
        x_k_minus_1 = x_k
        x_k = x_k_plus_1

    raise ValueError("Secant method did not converge within the maximum number of iterations.")

# Streamlit app
def main():
    st.title("Root Finding Methods")
    st.write("Developed and deployed by Abhirup Ghosh")
    method = st.selectbox("Choose the method", ["Bisection Method", "Newton-Raphson Method", "Secant Method"])

    func_str = st.text_input("Enter the function (in terms of x, e.g., 'x**2 - 4', 'math.sin(x)'):")

    if func_str:
        try:
            func = eval(f"lambda x: {func_str}")
        except SyntaxError:
            st.error("Invalid function syntax. Please enter a valid Python expression.")
            return
    else:
        st.error("Function input cannot be empty.")
        return

    tol = st.number_input("Enter the tolerance (tol):", value=1e-6, format="%.10f")

    if method == "Bisection Method":
        a = st.number_input("Enter the start of the interval (a):")
        b = st.number_input("Enter the end of the interval (b):")
        if st.button("Compute Root"):
            try:
                root = bisection_method(func, a, b, tol)
                st.success(f"Bisection Method Root: {root}")
            except ValueError as e:
                st.error(e)

    elif method == "Newton-Raphson Method":
        derivative_str = st.text_input("Enter the derivative of the function (in terms of x, e.g., '2*x', 'math.cos(x)'):")
        if derivative_str:
            try:
                func_derivative = eval(f"lambda x: {derivative_str}")
            except SyntaxError:
                st.error("Invalid derivative function syntax. Please enter a valid Python expression.")
                return
        else:
            st.error("Derivative input cannot be empty.")
            return

        initial_guess = st.number_input("Enter the initial guess:")
        if st.button("Compute Root"):
            root = newton_raphson_method(func, func_derivative, initial_guess, tol)
            st.success(f"Newton-Raphson Method Root: {root}")

    elif method == "Secant Method":
        x0 = st.number_input("Enter the first initial guess (x0):")
        x1 = st.number_input("Enter the second initial guess (x1):")
        if st.button("Compute Root"):
            try:
                root, iterations = secant_method(func, x0, x1, tol)
                st.success(f"Secant Method Root: {root}")
                st.info(f"Iterations: {iterations}")
            except ValueError as e:
                st.error(e)

if __name__ == "__main__":
    main()
