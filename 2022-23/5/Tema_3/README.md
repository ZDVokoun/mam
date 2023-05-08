# Téma 3 - úloha 1
Tento systém výtahů se skládá ze tří výtahů a je navrhnut tak, že
cestující ho může ovládat jen z patra, ve kterém stojí, nikoliv z výtahu
samotného. Tím pádem z každého stisknutého tlačítka získáme informace,
jaké patro má výtah navštívit (tam, kde cestující stojí) a kam se vrátit (místo,
kam se chce cestující dostat). Díky tomu se nemůže stát, že by se cestující
nemohl dostat do svého cílového patra.

Ve svém návrhu jsem zavedl několik optimalizací. První je ta, že řídící jednotka
bude posílat příkazy vždy tomu výtahu, který má ve frontě nejméně pater k
navštívení. Dále na úrovni výtahu si ukládám patra do dvou prioritních front.
Kdybychom však používali jen prioritní fronty, mohlo by dojít k tomu, že
by výtah navštívil nejdříve cílového patro cestujícího ještě předtím, než by ho
vůbec vyzvedl. Proto cílové patra ukládám ještě do slovníku listů, čímž
zařídím to, aby se cílové patra navštívili až po vyzvednutí cestujícího.
