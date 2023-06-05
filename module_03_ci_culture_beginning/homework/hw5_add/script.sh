#!/usr/bin/bash

pylint decrypt.py --output-format=json:quality_report.json,colorized --reports=y
pylint_res=$? 
echo "Код возврата анализатора кода = $pylint_res"
pytest tests/test_decrypt.py
pytest_res=$?
echo "Код возврата стартера тестов = $pytest_res"
if [[ pylint_res -eq 0 ]]; then
	if [[ pytest_res -eq 0 ]]; then 
	  echo ‘OK’
	else
 	  echo ‘Имеются ошибки’
 	fi
else 
  echo ‘OK’ 
fi
