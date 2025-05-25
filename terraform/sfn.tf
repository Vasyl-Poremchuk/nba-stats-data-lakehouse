# ================================================================================
# STEP FUNCTION & ORCHESTRATION.
# Step Function state machine & EventBridge scheduling resources.
# ================================================================================

# IAM Role for the Step Function.
resource "aws_iam_role" "step_function_role" {
  name = "step-function-data-pipeline-role"

  assume_role_policy = jsonencode(
    {
      "Version" = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "states.amazonaws.com"
          }
        }
      ]
    }
  )
}

# IAM Policy for the Step Function.
resource "aws_iam_role_policy" "step_function_policy" {
  name = "step-function-data-pipeline-policy"
  role = aws_iam_role.step_function_role.id

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "lambda:InvokeFunction"
          ]
          Resource = [
            aws_lambda_function.bronze_layer_trigger.arn
          ]
        },
        {
          Effect = "Allow"
          Action = [
            "glue:StartJobRun",
            "glue:GetJobRun",
            "glue:BatchStopJobRun"
          ]
          Resource = [
            aws_glue_job.silver_layer_season_etl_glue_job.arn,
            aws_glue_job.silver_layer_conference_etl_glue_job.arn,
            aws_glue_job.silver_layer_conference_stats_etl_glue_job.arn,
            aws_glue_job.silver_layer_team_stats_etl_glue_job.arn,
            aws_glue_job.silver_layer_player_stats_etl_glue_job.arn
          ]
        }
      ]
    }
  )
}

# Step Function State Machine.
resource "aws_sfn_state_machine" "nba_stats_data_pipeline" {
  name     = "nba-stats-data-pipeline"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode(
    {
      "Comment" : "Data transformation pipeline with Bronze, Silver, and Gold layers",
      "StartAt" : "LoadIntoBronzeLayerLambda",
      "States" : {
        "LoadIntoBronzeLayerLambda" : {
          "Type" : "Task",
          "Resource" : "arn:aws:states:::lambda:invoke",
          "Parameters" : {
            "FunctionName" : aws_lambda_function.bronze_layer_trigger.function_name,
            "Payload.$" : "$"
          },
          "ResultPath" : "$.bronzeResult",
          "Next" : "CheckStatus",
          "Retry" : [
            {
              "ErrorEquals" : [
                "Lambda.ServiceException",
                "Lambda.AWSLambdaException",
                "Lambda.SdkClientException"
              ],
              "IntervalSeconds" : 2,
              "MaxAttempts" : 3,
              "BackoffRate" : 2.0
            }
          ],
          "Catch" : [
            {
              "ErrorEquals" : [
                "States.TaskFailed"
              ],
              "Next" : "HandleFailure",
              "ResultPath" : "$.error"
            }
          ]
        },
        "CheckStatus" : {
          "Type" : "Choice",
          "Choices" : [
            {
              "Variable" : "$.bronzeResult.Payload.status",
              "StringEquals" : "SUCCESS",
              "Next" : "RunSilverLayerGlueJobsInParallel"
            },
            {
              "Variable" : "$.bronzeResult.Payload.status",
              "StringEquals" : "FAILURE",
              "Next" : "HandleFailure"
            }
          ],
          "Default" : "HandleFailure"
        },
        "RunSilverLayerGlueJobsInParallel" : {
          "Type" : "Parallel",
          "Branches" : [
            {
              "StartAt" : "SilverLayerSeasonETLGlueJob",
              "States" : {
                "SilverLayerSeasonETLGlueJob" : {
                  "Type" : "Task",
                  "Resource" : "arn:aws:states:::glue:startJobRun.sync",
                  "Parameters" : {
                    "JobName" : aws_glue_job.silver_layer_season_etl_glue_job.name
                  },
                  "End" : true,
                  "Retry" : [
                    {
                      "ErrorEquals" : [
                        "States.TaskFailed"
                      ],
                      "IntervalSeconds" : 30,
                      "MaxAttempts" : 2,
                      "BackoffRate" : 2.0
                    }
                  ]
                }
              }
            },
            {
              "StartAt" : "SilverLayerConferenceETLGlueJob",
              "States" : {
                "SilverLayerConferenceETLGlueJob" : {
                  "Type" : "Task",
                  "Resource" : "arn:aws:states:::glue:startJobRun.sync",
                  "Parameters" : {
                    "JobName" : aws_glue_job.silver_layer_conference_etl_glue_job.name
                  },
                  "End" : true,
                  "Retry" : [
                    {
                      "ErrorEquals" : [
                        "States.TaskFailed"
                      ],
                      "IntervalSeconds" : 30,
                      "MaxAttempts" : 2,
                      "BackoffRate" : 2.0
                    }
                  ]
                }
              }
            },
            {
              "StartAt" : "SilverLayerConferenceStatsETLGlueJob",
              "States" : {
                "SilverLayerConferenceStatsETLGlueJob" : {
                  "Type" : "Task",
                  "Resource" : "arn:aws:states:::glue:startJobRun.sync",
                  "Parameters" : {
                    "JobName" : aws_glue_job.silver_layer_conference_stats_etl_glue_job.name
                  },
                  "End" : true,
                  "Retry" : [
                    {
                      "ErrorEquals" : [
                        "States.TaskFailed"
                      ],
                      "IntervalSeconds" : 30,
                      "MaxAttempts" : 2,
                      "BackoffRate" : 2.0
                    }
                  ]
                }
              }
            },
            {
              "StartAt" : "SilverLayerTeamStatsETLGlueJob",
              "States" : {
                "SilverLayerTeamStatsETLGlueJob" : {
                  "Type" : "Task",
                  "Resource" : "arn:aws:states:::glue:startJobRun.sync",
                  "Parameters" : {
                    "JobName" : aws_glue_job.silver_layer_team_stats_etl_glue_job.name
                  },
                  "End" : true,
                  "Retry" : [
                    {
                      "ErrorEquals" : [
                        "States.TaskFailed"
                      ],
                      "IntervalSeconds" : 30,
                      "MaxAttempts" : 2,
                      "BackoffRate" : 2.0
                    }
                  ]
                }
              }
            },
            {
              "StartAt" : "SilverLayerPlayerStatsETLGlueJob",
              "States" : {
                "SilverLayerPlayerStatsETLGlueJob" : {
                  "Type" : "Task",
                  "Resource" : "arn:aws:states:::glue:startJobRun.sync",
                  "Parameters" : {
                    "JobName" : aws_glue_job.silver_layer_player_stats_etl_glue_job.name
                  },
                  "End" : true,
                  "Retry" : [
                    {
                      "ErrorEquals" : [
                        "States.TaskFailed"
                      ],
                      "IntervalSeconds" : 30,
                      "MaxAttempts" : 2,
                      "BackoffRate" : 2.0
                    }
                  ]
                }
              }
            }
          ],
          "Next" : "RunGoldLayerGlueJob",
          "Catch" : [
            {
              "ErrorEquals" : [
                "States.TaskFailed"
              ],
              "Next" : "HandlePartialFailure",
              "ResultPath" : "$.parallelError"
            }
          ]
        },
        "RunGoldLayerGlueJob" : {
          "Type" : "Task",
          "Resource" : "arn:aws:states:::glue:startJobRun.sync",
          "Parameters" : {
            "JobName" : aws_glue_job.gold_layer_gold_etl_glue_job.name
          },
          "ResultPath" : "$.goldResult",
          "Next" : "ProcessingComplete",
          "Retry" : [
            {
              "ErrorEquals" : [
                "States.TaskFailed"
              ],
              "IntervalSeconds" : 30,
              "MaxAttempts" : 2,
              "BackoffRate" : 2.0
            }
          ],
          "Catch" : [
            {
              "ErrorEquals" : [
                "States.TaskFailed"
              ],
              "Next" : "HandleGoldLayerFailure",
              "ResultPath" : "$.goldError"
            }
          ]
        },
        "ProcessingComplete" : {
          "Type" : "Pass",
          "Result" : {
            "status" : "SUCCESS",
            "message" : "All layer jobs completed successfully"
          },
          "End" : true
        },
        "HandleFailure" : {
          "Type" : "Pass",
          "Parameters" : {
            "status" : "FAILED",
            "message" : "Bronze layer processing failed",
            "originalError.$" : "$.bronzeResult.Payload"
          },
          "End" : true
        },
        "HandleGoldLayerFailure" : {
          "Type" : "Pass",
          "Result" : {
            "status" : "GOLD_LAYER_FAILED",
            "message" : "Gold layer processing failed, but silver layer completed successfully"
          },
          "End" : true
        },
        "HandlePartialFailure" : {
          "Type" : "Pass",
          "Result" : {
            "status" : "PARTIAL_FAILURE",
            "message" : "Some silver layer jobs failed"
          },
          "End" : true
        }
      }
    }

  )
}

# EventBridge Rule to trigger Step Function on a schedule.
resource "aws_cloudwatch_event_rule" "nba_data_pipeline_trigger" {
  name                = "nba-data-pipeline-trigger"
  description         = "Trigger NBA data pipeline annually"
  schedule_expression = "cron(0 0 2 11 ? *)" # Run at midnight on November 2nd
}

# EventBridge Target to trigger Step Function.
resource "aws_cloudwatch_event_target" "step_function_target" {
  rule      = aws_cloudwatch_event_rule.nba_data_pipeline_trigger.name
  target_id = "StepFunctionTarget"
  arn       = aws_sfn_state_machine.nba_stats_data_pipeline.arn
  role_arn  = aws_iam_role.eventbridge_step_function_role.arn
}

# IAM role for EventBridge to invoke Step Function.
resource "aws_iam_role" "eventbridge_step_function_role" {
  name = "eventbridge-step-function-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "events.amazonaws.com"
          }
        }
      ]
    }
  )
}

# IAM policy for EventBridge to start Step Function execution.
resource "aws_iam_role_policy" "eventbridge_step_function_policy" {
  name = "eventbridge-step-function-policy"
  role = aws_iam_role.eventbridge_step_function_role.id

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "states:StartExecution"
          ]
          Resource = [
            aws_sfn_state_machine.nba_stats_data_pipeline.arn
          ]
        }
      ]
    }
  )
}
