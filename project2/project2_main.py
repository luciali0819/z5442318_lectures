""" scaffold for project2


"""
# IMPORTANT: You should not import any other modules. This means that the
# only import statements in this module should be the ones below. In
# particular, this means that you cannot import modules inside functions.

import pandas as pd


# ----------------------------------------------------------------------------
#   Aux functions 
# ----------------------------------------------------------------------------
def read_dat(pth: str) -> pd.DataFrame:
    """ Create a data frame with the raw content of a .dat file.

    This function loads data from a `.dat` file into a data frame. It does not
    parse or clean the data, nor does it assign specific data types. All
    entries in the resulting data frame are stored as `str` instances, and all
    columns have an object `dtype`. This function can be used to load any
    `.dat` file.

    Parameters
    ----------
    pth: str
        The location of a .dat file. 

    Returns
    -------
    frame:
        A data frame. The dtype of each column is 'object' and the type of
        each element is `str`
    """
    # IMPORTANT: Please do not modify this function
    return pd.read_csv(pth, dtype=str).astype(str)


def str_to_float(value: str) -> float | None:
    """ This function attempts to convert a string into a float. It returns a
    float if the conversion is successful and None otherwise. 

    Parameters
    ----------
    value: str
        A string representing a float. Quotes and spaces will be ignored. 

    Returns
    -------
    float or None
        A float representing the string or None

    """
    # IMPORTANT: Please do not modify this function
    out = value.replace('"', '').replace("'", '').strip()
    try:
        out = pd.to_numeric(out)
    except:
        return None
    return float(out)


def fmt_col_name(label: str) -> str:
    """ Formats a column name according to the rules specified in the "Project
    Description" slide

    Parameters
    ----------
    label: str
        The original column label. See the "Project description" slide for
        more information

    Returns
    -------
    str:
        The formatted column label. 

    Examples
    --------

    - `fmt_col_name(' Close') -> 'close'

    - `fmt_col_name('Adj    Close') -> 'adj_close'

    """
    # <COMPLETE_THIS_PART>
    formatted_label = label.strip().lower()
    formatted_label = "_".join(formatted_label.split())
    return formatted_label


def fmt_ticker(value: str) -> str:
    """ Formats a ticker value according to the rules specified in the "Project
    Description" slide

    Parameters
    ----------
    value: str
        The original ticker value

    Returns
    -------
    str:
        The formatted ticker value.

    """
    # <COMPLETE_THIS_PART>
    return value.strip().replace('"', '').replace("'", '').upper()


def read_prc_dat(pth: str):
    """ This function produces a data frame with volume and return from a single
    `<PRICE_DAT>` file. 

    This function should clean the original data in `<PRICE_DAT>` as described
    in the "Project description" slide.

    Returns should be computed using adjusted closing prices.


    Parameters
    ----------
    pth: str
        The location of a <PRICE_DAT> file. This file includes price and
        volume information for different tickers and dates. See the project
        description for more information on these files.


    Returns
    -------
    frame: 
        A dataframe with formatted column names (in any order):
    
         Column     dtype
         ------     -----
         date       datetime64[ns]
         ticker     object
         return     float64
         volume     float64

    Notes
    -----

    Assume that there are no gaps in the time series of adjusted closing
    prices for each ticker.


    """
    # <COMPLETE_THIS_PART>
    df = read_dat(pth)

    df.columns = [fmt_col_name(col) for col in df.columns]
    df['ticker'] = df['ticker'].apply(fmt_ticker)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df['volume'] = df['volume'].apply(str_to_float)
    df['adj_close'] = df['adj_close'].apply(str_to_float)

    df = df.sort_values(by=['ticker', 'date'])
    df['return'] = df.groupby('ticker')['adj_close'].pct_change(fill_method=None)

    df = df[['date', 'ticker', 'return', 'volume']].dropna(subset=['return'])
    return df


def read_ret_dat(pth: str) -> pd.DataFrame:
    """ This function produces a data frame with volume and returns from a single
    `<RET_DAT>` file. 


    This function should clean the original data in `<RET_DAT>` as described
    in the "Project description" slide.

    Parameters
    ----------
    pth: str
        The location of a <RET_DAT> file. This file includes returns and
        volume information for different tickers and dates. See the project
        description for more information on these files.


    Returns
    -------
    frame: 
        A dataframe with columns (in any order):
    
          Column        dtype
          ------        -----
          date          datetime64[ns]
          ticker        object
          return        float64
          volume        float64

    Notes
    -----
    This .dat file also includes market returns. Market returns are 
    represented by a special ticker called 'MKT'

    """
    # <COMPLETE_THIS_PART>
    df = read_dat(pth)

    df.columns = [fmt_col_name(col) for col in df.columns]
    df['ticker'] = df['ticker'].apply(fmt_ticker)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df['volume'] = df['volume'].apply(str_to_float)
    df['return'] = df['return'].apply(str_to_float)

    df = df[['date', 'ticker', 'return', 'volume']].dropna(subset=['return'])
    return df


def mk_ret_df(
        pth_prc_dat: str,
        pth_ret_dat: str,
        tickers: list[str],
):
    """ Combine information from two sources to produce a data frame 
    ith stock and market returns according to the following rules:

    - Returns should be computed using information from <PRICE_DAT>, if
      possible. If a ticker is not found in the <PRICE_DAT> file, then returns
      should be obtained from the <RET_DAT> file.

    - Market returns should always be obtained from the <RET_DAT> file.

    - Only dates with available market returns should be part of the index.


    Parameters
    ----------
    pth_prc_dat: str
        Location of the <PRICE_DAT> file with price and volume information.
        This is the same parameter as the one described in `read_prc_dat`

    pth_ret_dat: str
        Location of the <RET_DAT> file with returns and volume information.
        This is the same parameter as the one described in `read_ret_dat`

    tickers: list
        A list of (possibly unformatted) tickers to be included in the output
        data frame. 

    Returns
    -------
    frame:
        A data frame with a DatetimeIndex and the following columns (in any
        order):

        Column      dtype 
        ------      -----
        <tic0>      float64
        <tic1>      float64
        ...
        <ticN>      float64
        <mkt>       float64


        Where `<tic0>`, ..., `<ticN>` are formatted column labels with tickers
        in the list `tickers`, and `<mkt>` is the formatted column label
        representing market returns.

        Should only include dates with available market returns.


    """
    # <COMPLETE_THIS_PART>
    prc_df = read_prc_dat(pth_prc_dat)
    ret_df = read_ret_dat(pth_ret_dat)

    formatted_tickers = [fmt_ticker(ticker) for ticker in tickers]
    prc_df = prc_df[prc_df['ticker'].isin(formatted_tickers)]
    ret_df = ret_df[ret_df['ticker'].isin(formatted_tickers + ['MKT'])]

    prc_df = prc_df.drop_duplicates(subset=['date', 'ticker'])

    prc_pivot = prc_df.pivot(index='date', columns='ticker', values='return')

    ret_df = ret_df[~ret_df['ticker'].isin(prc_df['ticker'].unique()) | (ret_df['ticker'] == 'MKT')]

    ret_pivot = ret_df.pivot(index='date', columns='ticker', values='return')

    combined_df = prc_pivot.combine_first(ret_pivot)

    combined_df = combined_df.dropna(subset=['MKT'])

    combined_df.columns = [col.lower() if col != 'MKT' else 'mkt' for col in combined_df.columns]

    columns = [col for col in combined_df.columns if col != 'mkt'] + ['mkt']
    combined_df = combined_df[columns]

    return combined_df
