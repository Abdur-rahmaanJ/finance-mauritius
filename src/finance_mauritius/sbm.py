import polars as pl


class SBM:
    csv_df = None 
    csv_info = None 

    @classmethod
    def process_csv(cls, path):
        info = {}
        with open(path) as file:
            line = file.readline()
            while line:
                
                if line.strip() == "":
                    line = file.readline()
                    continue
                
                line = line.strip().strip('\n').replace(',', '').casefold().replace('"', '')

                if line.startswith('account:'):
                    info['account_number'] = line[len('account:'):].split('-')[1].strip() 

                if line.startswith('date from'):
                    info['date_from'] = line[len('date from(mmddyyyy):'):].strip()

                if line.startswith('date to'):
                    info['date_to'] = line[len('date to(mmddyyyy):'):].strip()

                if line.startswith('transactions for'):
                    info['transactions_for'] = line[len('transactions for:'):].strip()

                if line.startswith('last n transactions'):
                    info['last_n_transactions'] = line[len('last n transactions:'):].strip()

                if line.startswith('instrument id'):
                    break

                
                line = file.readline()

        df = pl.read_csv(path, skip_rows=5)
        df = df.with_columns(pl.col("Debit Amount").str.replace(r",", ""))
        df = df.with_columns(pl.col("Debit Amount").fill_null(0.0))
        df = df.with_columns(pl.col("Credit Amount").str.replace(r",", ""))
        df = df.with_columns(pl.col("Credit Amount").fill_null(0.0))
        df = df.with_columns(pl.col("Balance").str.replace(r",", ""))


        df = df.with_columns(pl.col('Debit Amount').cast(pl.Decimal(scale=2, precision=None), strict=False))
        df = df.with_columns(pl.col('Credit Amount').cast(pl.Decimal(scale=2, precision=None), strict=False))
        df = df.with_columns(pl.col('Balance').cast(pl.Decimal(scale=2, precision=None), strict=False))

        df = df.with_columns(pl.col('Transaction Date').str.strptime(pl.Date,'%m,%d,%Y'))
        df = df.with_columns(pl.col('Value Date').str.strptime(pl.Date,'%m,%d,%Y'))

        info['money_in'] = float(df["Credit Amount"].sum())

        cls.csv_df = df 
        cls.csv_info = info

        return {
            'info': info,
            'df': df
        }
    

    @classmethod
    def csv_money_in(cls):
        if cls.csv_df is None:
            raise Exception('Please use SBM.process_csv first')
        groupby = cls.csv_df.group_by("Remarks").agg(pl.col("Credit Amount").sum())
        rows = dict(groupby.iter_rows())
        filtered_above_0 = dict(filter(lambda e:e[1]>0.0, rows.items() ) )

        return filtered_above_0
    
    @classmethod
    def csv_money_out(cls):
        if cls.csv_df is None:
            raise Exception('Please use SBM.process_csv first')
        groupby = cls.csv_df.group_by("Remarks").agg(pl.col("Debit Amount").sum())
        rows = dict(groupby.iter_rows())
        filtered_above_0 = dict(filter(lambda e:e[1]>0.0, rows.items() ) )

        return filtered_above_0