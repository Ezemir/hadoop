package br.com.vpsic;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class DieselReducer extends Reducer<Text, DoubleWritable, Text, DoubleWritable> {
    @Override
    protected void reduce(Text key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException {
        double soma = 0;
        int count = 0;
        for (DoubleWritable val : values) {
            soma += val.get();
            count++;
        }
        if (count > 0) {
            context.write(key, new DoubleWritable(soma / count));
        }
    }
}