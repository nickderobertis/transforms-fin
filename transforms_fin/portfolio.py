import datacode as dc
from pd_utils import portfolio
from sympy import Symbol


def portfolio_name_func(name: str, **kwargs) -> str:
    return name + ' Portfolio'


def portfolio_symbol_func(sym: Symbol, **kwargs) -> Symbol:
    sym_str = str(sym)
    new_sym_str = r'\text{Port}(' + sym_str + ')'
    sym = Symbol(new_sym_str)
    return sym


def portfolio_data_func(col: dc.Column, variable: dc.Variable, source: dc.DataSource, **kwargs) -> dc.DataSource:
    if 'portvar' in kwargs:
        raise ValueError('cannot pass portvar as variable will be transformed into portvar')

    if 'byvars' not in kwargs:
        by_vars = []
        other_indices = [col_idx for col_idx in col.indices if col_idx]
        if len(other_indices) > 0:
            # Got other indices
            for col_idx in other_indices:
                by_vars.extend(col_idx.variables)
        by_var_names = [var.name for var in by_vars]
        if by_var_names:
            kwargs['byvars'] = by_var_names

    # TODO: rework portfolio once pd_utils.portfolio supports using index
    orig_index_names = source.df.index.names
    source.df = portfolio(
        source.df.reset_index(),
        variable.name,
        **kwargs
    )

    source.df.drop([variable.name], axis=1, inplace=True)
    source.df.rename(columns={'portfolio': variable.name}, inplace=True)
    source.df.set_index(orig_index_names, inplace=True)
    return source


portfolio_transform = dc.Transform(
    'port',
    name_func=portfolio_name_func,
    data_func=portfolio_data_func,
    symbol_func=portfolio_symbol_func,
    data_func_target='source'
)