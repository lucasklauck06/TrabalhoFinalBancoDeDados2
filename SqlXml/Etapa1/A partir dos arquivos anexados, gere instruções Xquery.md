# Etapa1

## a-Retornar os dados da penúltima peça da árvore XML.
let $doc := doc("peca.xml")
return $doc//peca[last() - 1]

## b-Inserir um atributo com a data em todos os fornecimentos, a data deve ser inserida no formado YYYY-MM-DD.
for $f in doc("fornecimento.xml")//fornecimento
return insert node attribute data {'2025-11-18'} into $f

## c-Atualizar o status dos fornecedores de Londres para 50.
for $fornecedor in doc("fornecedor.xml")//fornecedor
where $fornecedor/Cidade = "LONDRES"
return replace value of node $fornecedor/Status with 50

## d-Retornar o código, a cidade e cor de todas as peças.
for $peca in doc("peca.xml")//peca
return 
  <peca_info>
    {$peca/Cod_Peca}
    {$peca/Cidade}
    {$peca/Cor}
  </peca_info>

## e-Obter o somatório das quantidades dos fornecimentos.
let $qtde := doc("fornecimento.xml")//fornecimento/Quantidade
return sum($qtde)

## f-Obter os nomes dos projetos de Paris.
for $proj in doc("projeto.xml")//projeto
where $proj/Cidade = "PARIS"
return $proj/Jnome/text()

## g-Obter o código dos fornecedores que forneceram pecas em maior quantidade.
let $fornecimentos := doc("fornecimento.xml")//fornecimento
let $max_qtde := max($fornecimentos/Quantidade)

for $f in $fornecimentos
where $f/Quantidade = $max_qtde
return $f/Cod_Fornec/text()

## h-Excluir os projetos da cidade de Atenas.
for $proj in doc("projeto.xml")//projeto
where $proj/Cidade = "ATENAS"
return delete node $proj

## i-Obter os nomes das peças e seus dados de fornecimento.
for $p in doc("peca.xml")//peca
return 
  <relatorio_peca>
    <nome>{data($p/PNome)}</nome>
    {
      for $f in doc("fornecimento.xml")//fornecimento
      where $f/Cod_Peca = $p/Cod_Peca
      return $f
    }
  </relatorio_peca>

## j-Obter o preço médio das peças.
let $precos := doc("peca.xml")//peca/Preco
return avg($precos)
