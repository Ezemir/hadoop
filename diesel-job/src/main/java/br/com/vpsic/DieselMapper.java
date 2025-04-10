package br.com.vpsic;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class DieselMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {
    private static final int ESTADO_INDEX = 1;
    private static final int PRODUTO_INDEX = 10;
    private static final int VALOR_VENDA_INDEX = 12;
    private static final Text DIESEL_SP = new Text("DIESEL_SP");

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        if (line.contains("Produto")) return; // Ignora o cabeçalho

        String[] campos = line.split(";");
        if (campos.length > VALOR_VENDA_INDEX) {
            String estado = campos[ESTADO_INDEX].trim().toUpperCase();
            String produto = campos[PRODUTO_INDEX].trim().toUpperCase();
            String valorStr = campos[VALOR_VENDA_INDEX].replace(",", ".").trim();

            if (produto.contains("DIESEL") && estado.equals("SP")) {
                try {
                    double valor = Double.parseDouble(valorStr);
                    context.write(DIESEL_SP, new DoubleWritable(valor));
                } catch (NumberFormatException ignored) {}
            }
        }
    }
}
