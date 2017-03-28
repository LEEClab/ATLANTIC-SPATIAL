# Database

## Description of database 

### 1. Landscape

### Source
- SOS Mata Atlântica

- MapBiomas

### Variables
- Percentage of native vegetation cover

  LSMetrics gera a porcentagem de cobertura numa janela ao redor de cada pixel

- Structural connectivity

  LSMetrics gera uma métrica chamada "Patch size", o tamanho de cada patch (ou conjunto de pixels de vegetação nativa, ou de qualquer tipo de cobertura) conectados estruturalmente;  gera tb "Fragment size" (o mesmo que patch size, mas sem contar corredores ou estuturas com largura menor do que o definido pelo usuário;  e gera uma medida chamada structural connectivity, a diferença em hectares entre Patch size e Fragment size;  se um patch tem um só fragmento, a conectividade estrutural é zero)

- Functional connectivity (0 - 1500 m)

  LSMetrics gera: "Total Functionally Connected Area", a área dos clusters de fragmentos funcionalmente conectados, dado uma capacidade de cruzar matrizes,  definida pelo usuario; E calcula a "functional connectivity", a diferença em hectares entre os tamanhos dos clusters e o patch size

- Core area

 LSMetrics também é possível calcular a core area dos fragmentos, dado uma distância de borda definida pelo usuario
 
 - Edge

  LSMetrics quantifica a area de borda total na paisagem, e tb a porcentagem de borda numa janela ao redor de cada pixel, dada uma extensão dessa janela;  para ambos, a distancia de borda é um parâmetro definido pelo usuario
        
- Heterogeneity

  LSMetrics calcula diversidade de Shannon - mas da pra facilmente modificar a medida de diversidade...

---

### 2. Relief

### Source
- Topodata (90 m)

### Variables
- Altitude

- Declivity

- Aspecty

- Accumulated flow

---

### 3. Climate

### Source
- Worldclim

- CHELSA

- EcoClimate

### Variables
- Temperature

- Precipitation


---
