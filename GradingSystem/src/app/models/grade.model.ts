export class Grade {
    constructor(
      public   id : number,
      public score : number,
      public  answer_id : number,
      public  student_id : number,
      public created_at ? : Date,
      public updated_at?: Date
    ) { }
  }
  /*Une interface est une structure de données qui décrit la forme d'un objet. Elle ne contient pas de logique ou de fonctionnalités, mais uniquement les noms et les types de propriétés. Les interfaces sont principalement utilisées pour définir des contrats ou des contraintes que les objets doivent respecter. Les interfaces sont également utilisées pour la déclaration de types dans TypeScript.

Un modèle, en revanche, est une classe qui contient des données ainsi que des méthodes qui effectuent des opérations sur ces données. Les modèles peuvent être considérés comme une représentation de la logique métier de l'application. Ils sont souvent utilisés pour encapsuler les données et les opérations qui leur sont associées, afin de faciliter la réutilisation et la maintenance du code.

En résumé, les interfaces sont utilisées pour décrire la forme ou la structure des données, tandis que les modèles encapsulent des données et des opérations qui leur sont associées. Les interfaces peuvent être utilisées pour définir des contrats que les modèles doivent respecter.

Dans Angular, les interfaces et les modèles sont souvent utilisés ensemble pour décrire la structure des données et encapsuler la logique métier associée à ces données. Par exemple, une interface peut être utilisée pour décrire la structure d'un objet de données, tandis qu'un modèle peut être utilisé pour encapsuler les opérations de traitement de ces données.*/