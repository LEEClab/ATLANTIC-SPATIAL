# Reports

## Rep 001 - 15/03/2017

- Dois processos para gerar variáveis de paisagem: 

      1. Séries temporaris (MapBiomas) - anos 2008-2015
  
      2. Integração das bases - melhor uso possível (SOS, MapBiomas e estados) - ano 2014 
  
- Três grupos de variáveis:
  
      1. Paisagem
      
        1.1  Porcentagem de cobertura vegetal nativo (LSMetrics gera a porcentagem de cobertura numa janela ao redor de cada pixel - isso é útil?)
        
        1.2. Conectividade estrutural 
        (LSMetrics gera uma métrica chamada "Patch size", o tamanho de cada patch (ou conjunto de pixels  
        de vegetação nativa, ou de qualquer tipo de cobertura) conectados estruturalmente;  
        gera tb "Fragment size" (o mesmo que patch size, mas sem contar corredores ou   
        estuturas com largura menor do que o definido pelo usuário;  
        e gera uma medida chamada structural connectivity, a diferença em hectares entre   
        Patch size e Fragment size;  se um patch tem um só fragmento, a conectividade  
        estrutural é zero) -> o que disso interessa?
        
        1.2.5. Com o LSMetrics também é possível calcular a core area dos fragmentos,  
        dado uma distância de borda definida pelo usuario -> isso interessa?
        
        1.3. Conectividade funcional (0 - 1500 m ?) (o LSMetrics gera: "Total Functionally Connected Area",  
        a área dos clusters de fragmentos funcionalmente conectados, dado uma capacidade de cruzar matrizes,  
        definida pelo usuario; E calcula a "functional connectivity", a diferença em hectares entre os  
        tamanhos dos clusters e o patch size.)
        
        1.4. Borda (LSMetrics quantifica a area de borda total na paisagem, e tb a porcentagem de borda  
        numa janela ao redor de cada pixel, dada uma extensão dessa janela;  
        para ambos, a distancia de borda é um parametro definido pelo usuario).
        
        1.5. Heterogeneidade (LSMetrics calcula diversidade de Shannon - mas  
        da pra facilmente modificar a medida de diversidade...)

      2. Relevo
        
        2.1 Altitude
        
        2.2 MDE
        
        2.3 Declividade
        
        2.4 Aspecto
        
        2.5 Fluxo acumulado
    
      3. Clima
        
        3.1 Temperatura
         
        3.2 Precipitação
        
        3.3 Cobertura de nuvens
        
        3.4 Radiação solar
        
        3.5 Velocidade do vento
        
        3.6 Pressão de vapor de água
    
    
- Organizar os scripts do GRASS para as variáveis de paisagem e relevo

- Baixar as variáveis de clima e relevo

- Bases do Paraguai e Argentina 

- Encontrar a legenda ofical do MapBiomas

- Fazer o mosaico do MapBiomas para todos os anos

---
