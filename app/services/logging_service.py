from app.models.llm_log import LLMLog

def log_request(db, user_email, model_name, prompt, response,
                tokens_input, tokens_output, cost, latency):

    log = LLMLog(
        user_id=user_email,
        model_name=model_name,
        prompt=prompt,
        response=response,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        cost=cost,
        latency=latency
    )

    db.add(log)
    db.commit()
