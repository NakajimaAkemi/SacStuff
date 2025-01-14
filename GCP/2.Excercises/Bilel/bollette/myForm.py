
from wtforms import Form, IntegerField,validators,StringField, FloatField, BooleanField, DateField, DateTimeField, SelectField, RadioField, PasswordField,TextAreaField, EmailField, URLField


class MyForm(Form):
    id = IntegerField('id', [validators.DataRequired(),validators.NumberRange(min=0,max=255)])
    nome = StringField('nome', [validators.DataRequired(),validators.length(max=10)])
    cognome = StringField('cognome', [validators.DataRequired(),validators.length(max=10)])
    cap = IntegerField('cap', [validators.DataRequired(),validators.NumberRange(min=0,max=50000)])

    
    
    



class GenericForm(Form):
    """
    Classe WTForm generica con i principali tipi di campi e validatori.
    """
    
    # Campi di Testo
    string_field = StringField('String Field', 
        [validators.Length(min=1, max=255, message="Deve essere compreso tra 1 e 255 caratteri.")]
    )
    
    # Campi Numerici
    integer_field = IntegerField(
        'Integer Field', 
        [validators.NumberRange(min=0, max=1000, message="Deve essere tra 0 e 1000.")]
    )
    float_field = FloatField(
        'Float Field', 
        [validators.NumberRange(min=0.0, max=1000.0, message="Deve essere tra 0.0 e 1000.0.")]
    )
    
    # Campi Booleani
    boolean_field = BooleanField('Boolean Field')
    
    # Campi per Date e Tempo
    date_field = DateField(
        'Date Field', 
        [validators.Optional()],
        format='%Y-%m-%d'
    )
    datetime_field = DateTimeField(
        'Datetime Field', 
        [validators.Optional()],
        format='%Y-%m-%d %H:%M:%S'
    )
    
    # Campi di Selezione
    select_field = SelectField(
        'Select Field', 
        choices=[('option1', 'Option 1'), ('option2', 'Option 2')]
    )
    radio_field = RadioField(
        'Radio Field', 
        choices=[('yes', 'Yes'), ('no', 'No')]
    )
    
    # Campi di Sicurezza
    password_field = PasswordField(
        'Password Field', 
        [validators.DataRequired(), validators.Length(min=6, message="Minimo 6 caratteri.")]
    )
    
    # Campi Testo Avanzati
    text_area_field = TextAreaField(
        'Text Area Field', 
        [validators.Optional(), validators.Length(max=500, message="Massimo 500 caratteri.")]
    )
    
    # Campi Speciali
    email_field = EmailField(
        'Email Field', 
        [validators.Email(message="Inserisci un'email valida.")]
    )
    url_field = URLField(
        'URL Field', 
        [validators.URL(message="Inserisci un URL valido.")]
    )
    
    # Validatori Comuni
    required_field = StringField(
        'Required Field', 
        [validators.DataRequired(message="Questo campo è obbligatorio.")]
    )
    optional_field = StringField(
        'Optional Field', 
        [validators.Optional()]
    )
    
    # Metodo di conversione in dizionario
    def to_dict(self):
        """
        Restituisce i dati del form sotto forma di dizionario.
        """
        return {field.name: field.data for field in self}

    # Metodo per popolare i campi con un dizionario
    def from_dict(self, data):
        """
        Popola i campi del form con un dizionario.
        """
        for field_name, value in data.items():
            if hasattr(self, field_name):
                getattr(self, field_name).data = value

    # Validazione con dati di richiesta
    def validate_on_submit(self, request_form):
        """
        Valida i dati provenienti dalla richiesta Flask.
        """
        return self.validate(request_form)
