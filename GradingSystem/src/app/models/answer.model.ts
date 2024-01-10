  export class Answer {
    constructor(
     
      public text_answer: string,
      public question_id :number,
      public student_id : number,
      public  _id? : number,
      public created_at ? : Date,
      public updated_at?: Date,
    ) { }
  }