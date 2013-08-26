
//Funcion ql que FUNCIONA y envia a una vista la especialidad seleccionada
$(document).on('ready', function() {
	$('#id_especialidad').on('change', function() { 
		var val = $('#id_especialidad option:selected').html();


		$.ajax({
			async:true,
			url:'ajaxespecialidad',
			data:'a='+val+'&csrfmiddlewaretoken=' + getCookie('csrftoken'),
			type:'post',
			dataType: 'html',
			beforeSend: function () {
				$('#id_dentista').empty()
				
			},
			success: function(respuesta) {
				hora(respuesta);
			},
			timeout: 8000,
			error: function () {
				alert('Ha ocurrido un error, por favor inténtelo nuevamente.');
			}
		})
	});
});
//Funcion ql que FUNCIONA y agrega los dentistas al selectbox
function hora(jdata){
	$('#id_dentista').append('<option value ="0">elija...</option>');
	var coso = JSON.parse( jdata );
    for (var i = 0; i < coso.length; i++){
		$('#id_dentista').append('<option value ="'+i+'">'+coso[i]+'</option>');
	};
}

//Funcion ql que FUNCIONA Muestra el calendario una vez que se cambia el select box del Dentista
$(document).on('ready',function(){
	$('#id_dentista').on('change',function(){
		$('div').removeClass('hidden hasDatepicker');
	});
});

//Funcion ql que FUNCIONA y una vez que se toca el calendario,agrega la tabla y la rellena con los botones
function juntando(numero_dia,numero_mes,mes,valor){
	$.ajax({
		async:true,
		url:'ajaxoferta',
		data:'a='+valor+'&csrfmiddlewaretoken=' + getCookie('csrftoken'),
		type:'post',
		dataType: 'html',
		beforeSend: function () {
		calendario(numero_dia,numero_mes,mes);	
		},
		success: function(respuesta) {
		rellenarhorarios(respuesta);
		},
		timeout: 8000,
		error: function () {
			alert('Error');
		}
	})
}
//Funcion ql que FUNCIONA y agrega los botones en los horarios disponibles
function rellenarhorarios(jdata){
	
	var coso = JSON.parse( jdata );
	    for (var i = 0; i < coso.length; i++){
		$('#'+coso[i]+'-'+coso[i+1]+'-'+coso[i+2]).append("<button onclick='javascript:bfuncion(this.id);' type='submit'class='chuncoco btn btn-primary' id='"+coso[i]+'-'+coso[i+1]+'-'+coso[i+2]+"'>Reservar</button>"
		);
	};
}

function bfuncion(ide){
	//alert('este es un click');
	
	var esp = $('#id_especialidad option:selected').html(); 
	var den = $('#id_dentista option:selected').html();

			$.ajax({
			async:true,
			url:'tomarhora',
			data:'idd='+ide+'&esp='+esp+'&den='+den+'&csrfmiddlewaretoken=' + getCookie('csrftoken'),
			type:'post',
			dataType: 'html',

			beforeSend: function () {

				
			},
			success:function(){
				 function redirection(){  
				  window.location ="http://localhost:8000/paciente";
				  }
				  redirection()
			},
			timeout: 8000,
			error: function () {
				alert('Ha ocurrido un error, por favor inténtelo nuevamente.');
			}
		})
}




var dias = [
	'Lunes'
	, 'Martes'
	, 'Miércoles'
	, 'Jueves'
	, 'Viernes'
];
var horarios = [
	'08:00'
	, '08:30'
	, '09:00'
	, '09:30'
	, '10:00'
	, '10:30'
	, '11:00'
	, '11:30'
	, '12:00'
	, '12:30'
	, '13:00'
	, '13.30'
	, '14:00'
	, '14:30'
	, '15:00'
	, '15:30'
	, '16:00'
	
];

//Funcion ql que FUNCIONA y agrega la tabla con la semana del mes
function calendario(numero_dia,numero_mes,mes){
	//alert(dato);
	var largo_semana = dias.length;
	mes=mes+1;

	var $grilla = $('#grilla');
	var $cabecera = $('#cabecera');
	$cabecera.empty();
	$grilla.empty();

	var primer_dia = numero_mes - numero_dia + 1;
	(function (){
		var $row = $('<tr></tr>');

		$row.append('<th>Bloque</th>');
		$.each(dias, function(idx, dia) {
			console.log(dia);
			var $col = $('<th> ' + dia + ' ' + (primer_dia + idx) + '</th>');
			$row.append($col);
		})

		$cabecera.append($row)
	})();

	$.each(horarios, function (idx, horario) {
		console.log(horario)
		var $row = $('<tr></tr>');
		var $horario = $('<td> ' + horario + '</td>')
		$row.append($horario);

		$.each(dias, function(idx_dia, dia){
			var $bloque = $('<td id="' + mes + '-' + (idx_dia + primer_dia) + '-' + idx + '"></td>');
			$row.append($bloque);
		});	

		
		$grilla.append($row);


	});
}




$(document).on('ready', function() {
	$('#dios').click(function() {
		var fecha= new Date();
		var mes=fecha.getMonth()+1;

		$.ajax({
			async:true,
			url:'dameoferta',
			data:'a='+mes+'&csrfmiddlewaretoken=' + getCookie('csrftoken'),
			type:'post',
			dataType: 'html',
			beforeSend: function () {	
			//alert('esta es mi oferta');			
				
			},
			success: function(respuesta) {
				ofertaahora();
			},
			timeout: 8000,
			error: function () {
				alert('Ha ocurrido un error, por favor inténtelo nuevamente.');
			}
		})
	});
});
function ofertaahora(){
	var dia=15;
	var ano=2013;
	//var mes=new Date();
	
	var aux= new Date();
	var mes=aux.getMonth();
	var fecha=new Date('2013',mes,'15');
	var numero_mes= mes+1;

	//alert('mifecha es : '+fecha);
	var numero_dia=fecha.getDay();


	//alert(dato);
	var largo_semana = dias.length;
	var $grilla2 = $('#grilla2');
	var $cabecera2 = $('#cabecera2');
	$cabecera2.empty();
	$grilla2.empty();

	var primer_dia = numero_mes - numero_dia + 1;
	(function (){
		var $row = $('<tr></tr>');

		$row.append('<th>Bloque</th>');
		$.each(dias, function(idx, dia) {
			console.log(dia);
			var $col = $('<th> ' + dia + '</th>');
			$row.append($col);
		})

		$cabecera2.append($row)
	})   ();

	$.each(horarios, function (idx, horario) {
		console.log(horario)
		var $row = $('<tr></tr>');
		var $horario = $('<td> ' + horario + '</td>')
		$row.append($horario);

		$.each(dias, function(idx_dia, dia){
			var $bloque = $('<td id="' + numero_mes + '-' + (idx_dia + primer_dia) + '-' + idx + '"></td>');
			$row.append($bloque);
		});	

		
		$grilla2.append($row);
		//$grilla3.append('esto es un append');
	});

}


$(document).on('ready', function() {
	$('#dios2').click(function() {
		var fecha= new Date();
		var mes=fecha.getMonth()+2;
		$.ajax({
			async:true,
			url:'dameoferta',
			data:'a='+mes+'&csrfmiddlewaretoken=' + getCookie('csrftoken'),
			type:'post',
			dataType: 'html',
			beforeSend: function () {				
				
			},
			success: function(respuesta) {
				ofertasiguiente();
				rellenaroferta(respuesta);
			},
			timeout: 8000,
			error: function () {
				alert('Ha ocurrido un error, por favor inténtelo nuevamente.');
			}
		})
	});
	function prueba(){

		alert('esto es una prueba e.e');
	}
});


function ofertasiguiente(){
	var dia=15;
	var ano=2013;
	//var mes=new Date();
	
	var aux= new Date();
	var mes=aux.getMonth()+1;
	var fecha=new Date('2013',mes,'15');
	var numero_mes= mes+1;

	//alert('mifecha es : '+fecha);
	var numero_dia=fecha.getDay();


	//alert(dato);
	var largo_semana = dias.length;
	var $grilla2 = $('#grilla3');
	var $cabecera2 = $('#cabecera3');
	$cabecera2.empty();
	$grilla2.empty();

	var primer_dia = numero_mes - numero_dia + 1;
	(function (){
		var $row = $('<tr></tr>');

		$row.append('<th>Bloque</th>');
		$.each(dias, function(idx, dia) {
			console.log(dia);
			var $col = $('<th> ' + dia + '</th>');
			$row.append($col);
		})

		$cabecera2.append($row)
	})   ();

	$.each(horarios, function (idx, horario) {
		console.log(horario)
		var $row = $('<tr></tr>');
		var $horario = $('<td> ' + horario + '</td>')
		$row.append($horario);

		$.each(dias, function(idx_dia, dia){
			var $bloque = $('<td id="' + numero_mes + '-' + (idx_dia + primer_dia-1) + '-' + idx + '"></td>');
			$row.append($bloque);
		});	

		
		$grilla2.append($row);
		//$grilla3.append('esto es un append');
	});

}

function rellenaroferta(jdata){
	
	var coso = JSON.parse( jdata );
	    for (var i = 0; i < coso.length; i++){
		$('#'+coso[i]+'-'+coso[i+1]+'-'+coso[i+2]).append("<button type='button' class='btn btn-info'></button>"
		);
	};
}

function validarRut(numero,dv) {
    if(!isNaN(numero) || numero.length == 0 || numero.length > 8 ) {
        return false;
    } else {
        if(getDV(numero) == dv) return true;
    }
    return false;
}
function getDV(numero) {
    nuevo_numero = numero.toString().split("").reverse().join("");
    for(i=0,j=2,suma=0; i < nuevo_numero.length; i++, ((j==7) ? j=2 : j++)) {
        suma += (parseInt(nuevo_numero.charAt(i)) * j); 
    }
    n_dv = 11 - (suma % 11);
    return ((n_dv == 11) ? 0 : ((n_dv == 10) ? "K" : n_dv));
}
          