			window.onload =  function(){
			
			$('.dbDrop').prop("selectedIndex", 0);
			$('.tables').prop("selectedIndex", 0);
			$('.columns').prop("selectedIndex", 0);
			$('.operator').prop("selectedIndex", 0);

			$('.tables').prop("disabled", true);
			$('.columns').prop("disabled", true);
			$('.querySubmit').prop("disabled", true);
						  
			$('.inputCheck').prop("checked", true);
			$('.inputCheck1').prop("checked", false);

			$('.inputVal').val('');
			
			};	
			
			function delFunction() {
				
				$.ajax({ 
					url: 'http://localhost:5000/getConnDel', 
					type: 'GET', 
					success: function(response){ 
						console.log(response)
					} 
				});				
				
			};
			
			function updateWhereFlag1() {
				if(!$('.inputCheck').is(":checked")){
					$('.inputCheck1').prop("checked", false);
				};			
			};				
			
			function updateWhereFlag() {
				$('.inputCheck1').prop("checked", true);				
			};			
		
            $(document).ready(function() {
                $('.dbDrop').select2();
                $('.tables').select2({placeholder: "Select Table"});
                $('.columns').select2({placeholder: "Select Column"});
                $('.operator').select2();
            });

			function jsFunction() {
				delFunction();
				$('.tables').prop("disabled", true);
				$('.columns').prop("disabled", true);
				$('.inputCheck').prop("checked", true);
				$('.inputCheck1').prop("checked", false);
				chosenEnv = document.getElementById("env").value;
				console.log(chosenEnv);
				$.ajax({ 
					url: 'http://localhost:5000/dbConnect', 
					type: 'POST', 
					data: {"myData": chosenEnv},
					success: function(response){ 
						console.log(response);
						getTable();
					} 
				});	
			};		

			function getColumn(){
				$('.columns').prop("disabled", true);
				var tableName = $(".tables option:selected").text();
				var updatedURL = 'http://localhost:5000/getColumn/' + tableName;
				$.ajax({ 
					url: updatedURL, 
					type: 'GET', 
					success: function(response){ 
						console.log(response["data"])
						$('.columns').empty();
						$('.columns').append(
							$('<option></option>').val("default").html("Select Column")
						);						
						$.each(response["data"], function(val, text) {
							$('.columns').append(
								$('<option></option>').val(val).html(text)
							);
						});
						$('.columns').prop("disabled", false);
					} 
				});					
			};

			
			function getTable() {
				$.ajax({ 
					url: 'http://localhost:5000/getTable', 
					type: 'GET', 
					success: function(response){ 
						console.log(response["data"])
						$('.tables').empty();
						$('.tables').append(
							$('<option></option>').val("default").html("Select Table")
						);								
						$.each(response["data"], function(val, text) {
							$('.tables').append(
								$('<option></option>').val(val).html(text)
							);
						});
						$('.tables').prop("disabled", false);
						$('.querySubmit').prop("disabled", false);
					} 
				});	
			};
			
			function outputResult() {
				var input1 = $('.inputCheck').is(":checked");
				var input2 = $('.inputVal').val();
				var input3 = $('.inputCheck1').is(":checked");
				var input4 = $('.query').val();
				var input5 = $(".tables option:selected").text();
				var input6 = $(".columns option:selected").text();
				var input7 = $(".operator option:selected").text();
				var value_data = {"selectAll": input1, 
					"colValue": input2, 
					"conditional": input3, 
					"query": input4,
					"tableName": input5,
					"columnName": input6,
					"operator": input7
					};
				$.ajax({ 
					url: 'http://localhost:5000/outputResult', 
					type: 'POST',
					data: JSON.stringify(value_data),
					success: function(response){
						$('.queryOutput').empty();
						$('.queryOutput').append(response);
						$('table.resultTable th').css({'border':'1px solid #ddd', 'padding':'5px', 'background':'#6499be', 'color':'#fff', 'text-align':'left'});
						$('table.resultTable td').css({'border':'1px solid #ddd', 'padding':'5px', 'font-family':'Calibri', 'text-align':'left'});
						$('table.resultTable tr:nth-child(even)').css({'background':'#f2f2f2'});
						window.scrollTo(0, 550);
						console.log(response);
					} 
				});	
			};			