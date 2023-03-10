from numpy import around, empty, sum, mean, std, square, divide
from .data_generation import data_generation


def run_erm_weight_finding(
    alpha: float,
    measure_fun,
    find_coefficients_fun,
    n_features: int,
    repetitions: int,
    measure_fun_args,
    find_coefficients_fun_args,
):
    all_gen_errors = empty((repetitions,))

    for idx in range(repetitions):
        xs, ys, _, _, ground_truth_theta = data_generation(
            measure_fun,
            n_features=n_features,
            n_samples=max(int(around(n_features * alpha)), 1),
            n_generalization=1,
            measure_fun_args=measure_fun_args,
        )

        print(xs.shape, ys.shape)

        estimated_theta = find_coefficients_fun(ys, xs, *find_coefficients_fun_args)

        all_gen_errors[idx] = divide(sum(square(ground_truth_theta - estimated_theta)), n_features)

        del xs
        del ys
        del ground_truth_theta

    error_mean, error_std = mean(all_gen_errors), std(all_gen_errors)
    print(alpha, "Done.")

    del all_gen_errors

    return error_mean, error_std
