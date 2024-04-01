import polars as pl


class MCB:
    csv_df = None 
    csv_info = None

    @classmethod
    def process_csv(path):

        info = {

        }

        with open(path) as file:
            line = file.readline()
            while line:
                
                if line.strip() == "":
                    line = file.readline()
                    continue
                
                line = line.strip().strip('\n').strip('"').casefold()
                if line[:len('account number')] =="account number":
                    info['account_number'] = line[len('account number'):].strip()

                if line[:len('account currency')] =="account currency":
                    info['account_currency'] = line[len('account currency'):].strip().upper()

                if line[:len('opening balance')] =="opening balance":
                    info['opening_balance'] = line[len('opening balance'):].strip().replace(',', '')

                if line[:len('closing balance')] =="closing balance":
                    info['closing_balance'] = line[len('closing balance'):].strip().replace(',', '')

                if line[:len('specified period')] =="specified period":
                    info['specified_period'] = line[len('specified period'):].strip().strip('()')

                if line[:len('transaction date')] =="transaction date":
                    break

                
                line = file.readline()

        df = pl.read_csv(path, skip_rows=14)
        df = df.drop_nulls()
        df = df.with_columns(pl.col('Value Date').str.strptime(pl.Date,'%d-%b-%Y'))
        df = df.with_columns(pl.col('Transaction Date').str.strptime(pl.Date,'%d-%b-%Y'))
        df = df.with_columns(pl.col("Money out").str.replace(r",", ""))
        df = df.with_columns(pl.col("Money in").str.replace(r",", ""))
        df = df.with_columns(pl.col('Money out').cast(pl.Float32, strict=False))
        df = df.with_columns(pl.col('Money in').cast(pl.Float32, strict=False))

        info['money_in'] = df['Money in'].sum()
        info['money_out'] = df['Money out'].sum()

        
        # x = df.group_by("Description").agg(pl.col("Money in").sum())
        # print(dict(x.iter_rows()))

        return {
            'df': df,
            'info': info
        }


