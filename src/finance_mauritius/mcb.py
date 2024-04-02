import polars as pl


class MCB:
    csv_df = None 
    csv_info = None

    @classmethod
    def process_csv(cls, path):

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
        df = df.with_columns(pl.col('Money out').cast(pl.Decimal(scale=2, precision=None), strict=False))
        df = df.with_columns(pl.col('Money in').cast(pl.Decimal(scale=2, precision=None), strict=False))

        info['money_in'] = df['Money in'].sum()
        info['money_out'] = df['Money out'].sum()

        
        # x = df.group_by("Description").agg(pl.col("Money in").sum())
        # print(dict(x.iter_rows()))

        cls.csv_df = df 
        cls.csv_info = info

        return {
            'df': df,
            'info': info
        }
    
    @classmethod
    def csv_money_in(cls):
        if cls.csv_df is None:
            raise Exception('Please use MCB.process_csv first')
        groupby = cls.csv_df.group_by("Description").agg(pl.col("Money in").sum())
        rows = dict(groupby.iter_rows())
        filtered_above_0 = dict(filter(lambda e:e[1]>0.0, rows.items() ) )

        return filtered_above_0
    
    @classmethod
    def csv_money_out(cls):
        if cls.csv_df is None:
            raise Exception('Please use MCB.process_csv first')
        groupby = cls.csv_df.group_by("Description").agg(pl.col("Money out").sum())
        rows = dict(groupby.iter_rows())
        filtered_above_0 = dict(filter(lambda e:e[1]>0.0, rows.items() ) )

        return filtered_above_0



