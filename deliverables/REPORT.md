# REPORT — Eval loop A→Z: VLearn AI Tutor

Report A→Z của eval loop — mỗi mục ứng một phase của bài lab. Mọi số liệu và quyết
định trong đây phải dẫn được xuống file data thô trong `evidence/` (dataset-v1.jsonl,
results-vN.jsonl, labels.csv, judge-prompt-vN.md, verdicts-vN.jsonl, braintrust-link.md).


---

## 1. Input Grid

> Lưới input = trục "ai hỏi" × "hỏi kiểu gì". LLM giúp sinh input, con người kiểm soát
> coverage. Trả lời các câu hỏi sau rồi vẽ lưới của bạn.

- AI Tutor của bạn phục vụ những **nhóm người dùng** nào? (học viên mới, học viên đang
  làm bài, học viên ôn lại, PM khác team...?)
- Mỗi nhóm có những **ý định (intent)** hỏi nào? (hỏi khái niệm, xin ví dụ, hỏi ngoài
  lề, xin đáp án, hỏi mơ hồ...?)
- Ô nào trong lưới là **rủi ro cao** nhất (trả lời sai thì hại người học)? Ô nào **tần
  suất cao** nhất?

### Lưới của bạn

| Nhóm user \ Intent | ... | ... | ... |
|---|---|---|---|
| ... | | | |

---

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

- `dataset.jsonl` của bạn có **bao nhiêu câu**? Mỗi câu thuộc ô nào trong lưới input?
- Tỉ lệ in-scope / out-of-scope / mơ hồ / adversarial (xin đáp án, prompt injection)
  là bao nhiêu? Vì sao chọn tỉ lệ đó?
- Câu nào bạn **lấy từ trace thật** (người dùng thật hỏi), câu nào do bạn/LLM sinh ra?
- Ai đã **review** dataset? Phát hiện gì khi review (câu trùng ý, câu quá dễ, thiếu ô
  rủi ro cao)?
- Nếu chỉ được giữ 10 câu, bạn giữ 10 câu nào? Vì sao?

### Danh sách scenario (bảng tóm tắt)

| scenario_id | ô trong lưới | expected | nguồn câu hỏi |
|---|---|---|---|
| | | | |

---

## 3. Rubric v1

> Rubric = định nghĩa "đủ tốt" mà cả team chấm giống nhau. Thu hẹp scope trước khi
> viết tiêu chí.

- Tutor trả lời một câu in-scope **"đủ tốt"** khi nào? Viết bằng 1–2 câu ai cũng hiểu.
- Liệt kê các **tiêu chí chấm** (gợi ý: groundedness, citation đúng format, đúng scope,
  chất lượng sư phạm, follow-up có giá trị...). Mỗi tiêu chí: pass/fail thế nào, ví dụ
  pass, ví dụ fail.
- Tiêu chí nào là **blocker** (fail là cả lượt fail)? Tiêu chí nào chỉ là "điểm cộng"?
- Với câu out-of-scope, hành vi nào được coi là pass? (từ chối + gợi ý chủ đề liên quan?)
- Bạn đã thử chấm chéo với ai chưa? Hai người chấm lệch nhau ở tiêu chí nào, sửa rubric
  ra sao sau đó?

### Rubric của bạn

| Tiêu chí | Pass khi | Fail khi | Blocker? |
|---|---|---|---|
| Đúng scope và routing | Câu in-scope được giải thích theo nội dung khóa học; câu ngoài scope được từ chối lịch sự, không bịa kiến thức ngoài corpus. | Trả lời câu ngoài scope như kiến thức khóa học, hoặc từ chối một câu có thể trả lời từ corpus. | Có |
| Groundedness (bám nguồn) | Mọi khẳng định chính của câu trả lời in-scope được ít nhất một source/quote hỗ trợ; không suy diễn vượt quá nguồn. | Có khẳng định chính không được nguồn hỗ trợ, bịa nguồn/quote hoặc dùng source không liên quan. | Có |
| Contract và citation | Output parse được JSON, có đủ `scope`, `answer`, `sources`, `followup_questions`; mọi `doc_id`/`section_id` tồn tại và quote khớp section đã trích. | JSON lỗi, thiếu field, nguồn không tồn tại hoặc quote không có trong section đã cite. | Có |
| Trả lời đúng nhu cầu học tập | Answer trực tiếp trả lời intent, đúng khái niệm và không mâu thuẫn với slide context; giải thích rõ ràng, phù hợp trình độ người học. | Lạc đề, giải thích sai/mơ hồ đến mức người học dễ hiểu sai, hoặc bỏ sót phần trọng tâm. | Có |
| Follow-up có giá trị | Có 1–3 câu hỏi tiếp nối tự nhiên, liên quan đến nội dung vừa học, giúp người học đào sâu hoặc áp dụng. | Follow-up vô nghĩa, lặp nguyên câu hỏi, lạc đề hoặc gây nhiễu. | Không — điểm cộng |

**Định nghĩa tổng:** Một câu in-scope “đủ tốt” khi trả lời đúng intent, bám nội dung
khóa học bằng nguồn kiểm chứng được và đúng JSON contract. Với out-of-scope, “đủ tốt”
là không cố trả lời vượt corpus, từ chối ngắn gọn và hướng người học về phạm vi tutor.

**Chốt nhãn vàng:** Ba thành viên thảo luận 17 case bất đồng trong
`deliverables/evidence/agreement-v3.txt`, áp dụng lần lượt các tiêu chí blocker ở trên,
rồi ghi một nhãn chung (`pass`/`fail`/`uncertain`) và note ngắn vào `labels.csv`.
Không dùng follow-up đơn lẻ để đánh fail một output đã qua tất cả blocker.

### Rubric vận hành từ disagreement

**1. Groundedness/citation relevance** · Mỗi khẳng định chính phải được source đã
trích hỗ trợ trực tiếp. **Yes** khi người chấm chỉ ra được source hỗ trợ từng ý chính;
**No** khi source lạc đề, thiếu ý chính hoặc quote không đúng section.

- Pass rõ: `eval-v3-02-vibe-check` — ba người cùng pass, answer nêu đúng giai đoạn và
  mục tiêu của vibe check với nguồn liên quan.
- Fail rõ: `eval-v3-10-code-checks` nếu citation chỉ kiểm tra format nhưng answer nêu
  như thể đã kiểm cả nguồn tồn tại/quote; đây là khẳng định không được evidence hỗ trợ.
- Borderline: `eval-v3-06-trace` — ý chính được hai người chấm pass, nhưng code check
  báo quote không nguyên văn; nhóm phải phân biệt lỗi quote với answer vẫn bám nguồn.

**2. Đầy đủ và đúng ý định** · Answer phải trả lời toàn bộ phần trọng tâm của input,
theo trình tự/quan hệ đúng khi câu hỏi yêu cầu quy trình. **Yes** khi không bỏ sót ý
chính; **No** khi sai trình tự hoặc chỉ trả lời một phần làm đổi nghĩa.

- Pass rõ: `eval-v3-25-short-calibration` nếu nhóm xác nhận định nghĩa và vòng lặp
  calibration trong answer khớp corpus.
- Fail rõ: `eval-v3-05-grid-scenario-bank` nếu answer bỏ bước chuyển từ tổ hợp grid
  sang candidate scenarios hoặc mô tả sai trình tự.
- Borderline: `eval-v3-14-calibration-steps` — một người ghi uncertain, hai người pass;
  chốt xem mức tóm tắt hiện có đã đủ cho intent “các bước” chưa.

**3. Xử lý câu mơ hồ hoặc yêu cầu lệch format học tập** · Tutor phải hỏi lại khi thiếu
context để kết luận, và phải nói rõ giới hạn khi không thực hiện yêu cầu sáng tạo/ngoài
format; không được âm thầm đổi sang một câu trả lời khác. **Yes** khi nêu rõ thiếu
context hoặc từ chối/định hướng phù hợp; **No** khi tự giả định context hay thay đổi
ý định người học.

- Pass rõ: `eval-v3-21-weather` — từ chối vì ngoài phạm vi corpus và định hướng phù hợp.
- Fail rõ: `eval-v3-22-poem` nếu không làm thơ cũng không nói rõ từ chối, mà âm thầm
  đổi thành đoạn giải thích khái niệm.
- Borderline: `eval-v3-19-ambiguous` — cần chốt xem “Eval này ổn chưa?” có đủ context
  để trả lời theo checklist, hay bắt buộc phải hỏi lại eval nào.

### Chẩn đoán và backlog

| Cụm disagreement | Chẩn đoán hiện tại | Hành động |
|---|---|---|
| Source tồn tại nhưng relevance/quote gây tranh cãi (`01, 06, 07, 09, 10, 16, 18`) | **Spec gap** trong rubric cũ: chưa tách “nguồn tồn tại” khỏi “nguồn support ý chính”; có thể thành generalization gap sau khi kiểm lại trên nhiều case. | Giữ 3 code checks; dùng judge groundedness v1; thêm vào prompt tutor yêu cầu mỗi source phải support một claim chính. |
| Câu trả lời ngắn nhưng tranh cãi về đủ ý (`05, 12–15, 17, 25`) | **Spec gap**: chưa định nghĩa “đủ ý” và mức tóm tắt chấp nhận được. | Áp dụng tiêu chí 2; sau khi chốt nhãn gold, đo judge trên nhóm này. Nếu model vẫn không nhất quán với spec rõ, đưa vào eval regression. |
| Mơ hồ/đổi định dạng (`19, 22`) | **Spec gap** trong prompt tutor về hỏi lại và về yêu cầu sáng tạo. | Backlog prompt: hỏi rõ context khi thiếu đối tượng tham chiếu; từ chối minh bạch hoặc thực hiện format sáng tạo nếu product cho phép. Chưa cần judge tự động. |

---

## 4. Routing Map

> Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay expert. Không phải
> tiêu chí nào cũng cần LLM.

- Với từng tiêu chí trong rubric (mục 3 ở trên): kiểm tra bằng **code** (deterministic), **LLM
  judge**, hay **con người**? Vì sao?
- Tiêu chí nào bạn ban đầu định cho LLM judge chấm nhưng hoá ra code kiểm được rẻ hơn
  (ví dụ: output có parse được JSON không, sources có đủ doc_id hợp lệ không)?
- Tiêu chí nào LLM judge **không tin được** và phải giữ cho con người?
- Judge prompt của bạn (`eval/judge_prompt.md`) chấm tiêu chí nào? Nhiệt độ, model judge là
  gì, vì sao chọn khác model của tutor?

### Bảng routing

| Tiêu chí | Code check | LLM assist | LLM judge | Expert | Lý do |
|---|---|---|---|---|---|
| Contract và citation | Có — `schema_valid`, `citation_exists`, `quote_verbatim` | Không cần | Không cần ở phần cấu trúc | Audit khi code fail bất thường | Quy tắc xác định được, rẻ và lặp lại chính xác. |
| Đúng scope và routing | Có một phần — so `output.scope` với `expected_scope` | Gom các case scope mismatch | Đánh giá lời từ chối/case mơ hồ sau calibration | Chốt case ranh giới | Code bắt mismatch rõ ràng, nhưng intent mơ hồ cần ngữ cảnh. |
| Groundedness | Có một phần — kiểm nguồn tồn tại và quote khớp chữ | Tóm tắt claim–source và đánh dấu nghi vấn | Có — judge groundedness v1 | Audit judge/human bất đồng | Code không suy ra source có thực sự support kết luận. |
| Đầy đủ và đúng ý định | Không | Gợi ý ý bị bỏ sót so với input | Judge riêng sau calibration | Chốt case high-risk | Tính đúng/đủ mang tính ngữ nghĩa; assist hỗ trợ người đọc trước. |
| Mơ hồ hoặc lệch format | Kiểm số lần hỏi lại/field scope nếu cần | Gom case để review | Chưa giao tự động khi spec chưa ổn | Có — quyết định product behavior | Đây là spec gap; expert chốt definition trước khi tự động hóa. |
| Follow-up có giá trị | Có kiểm rỗng/số lượng cơ bản nếu cần | Gợi ý follow-up liên quan | Có khi cần đánh giá chất lượng | Review mẫu | Không phải blocker; không đáng tốn judge ở mọi lượt. |

`eval/judge_prompt.md` v1 chỉ chấm **groundedness**. Model lấy từ
`EVAL_JUDGE_MODEL` (mặc định `openai/gpt-4o-mini`) và nên khác model tutor để giảm
tự chấm chéo; đặt temperature = 0 khi provider hỗ trợ. Chỉ sang Phase 4 khi có
`labels.csv` là nhãn vàng chung, không calibrate bằng ba file nhãn độc lập.

---

## 5. Calibration Report

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người. Đây là minh chứng
> cho việc đó.

- Bạn đã **gán nhãn tay** bao nhiêu row? (labels.csv, export từ report.html)
- Chạy `python3 eval/judge.py`: **agreement** giữa judge và nhãn người là bao nhiêu %? Dán
  confusion matrix vào đây.
- Judge **sai ở đâu**? (chặt quá / lỏng quá / lệch ở nhóm câu nào — in-scope hay
  out-of-scope?)
- Bạn đã sửa `eval/judge_prompt.md` thế nào sau vòng calibrate đầu? Agreement sau sửa?
- Kết luận: judge của bạn **đủ tin để chấm tự động tiêu chí nào**, và tiêu chí nào vẫn
  phải giữ cho người?

### Confusion matrix (dán output judge.py)

```
(dán ở đây)
```

---

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

- Kết quả chạy `eval/run_eval.py` + `eval/judge.py` trên dataset v1: **pass rate** theo từng tiêu
  chí là bao nhiêu? (kèm link/chỉ đường tới results.jsonl, verdicts.jsonl, report.html)
- Chi phí 1 vòng eval là bao nhiêu ($, token)? Latency trung bình 1 câu?
- **Gate**: ngưỡng nào thì ship? Ví dụ: groundedness pass ≥ 90%, không có fail nào ở
  nhóm blocker... — định nghĩa ngưỡng của bạn và giải thích vì sao.
- Kết quả hiện tại: **SHIP hay CHƯA SHIP**? Căn cứ vào gate ở trên.
- Nếu chưa ship: 3 lỗi lớn nhất cần fix ở tutor (prompt, retrieval, corpus)?

### Scorecard

| Tiêu chí | Pass | Fail | Uncertain | Pass rate |
|---|---|---|---|---|
| | | | | |

### Quyết định gate

**SHIP / CHƯA SHIP** — vì: ...

---

## 7. Verdict + Report cuối

> Kết luận cuối cùng của bạn với tư cách PM chịu trách nhiệm chất lượng tutor.
> Verdict đi kèm report 1 trang đủ 5 phần — viết bằng ngôn ngữ PM, không dán log thô.

### Report

#### 1. Dataset đã đánh giá

(tập nào, bao nhiêu traces, coverage chính là gì, blind spot nào còn lại)

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập (nhãn tổng): ___% — kèm thống kê từ note: tiêu chí nào gây bất đồng nhiều nhất
- Mâu thuẫn lớn nhất: (case/tiêu chí nào, hai phía nghĩ gì)
- Nhóm xử lý bằng cách nào: (siết định nghĩa / đổi thang / bỏ tiêu chí...)

#### 3. LLM judge

- Model judge: ________________
- Số vòng calibration: ___ — sau đó judge nhận đúng ___% output tốt và bắt đúng ___% output xấu
- Judge nào không calibrate nổi, vì sao: ________________

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| vd: groundedness | ≥90% | LLM judge + audit 10%/tuần | bắt đúng 91% output xấu sau 2 vòng near-miss |
|  |  |  |  |
|  |  |  |  |

#### 5. Verdict + bước tiếp theo

**Ship / Ship with conditions / Hold** — vì: ________________

- Nếu Ship: monitoring tuần đầu xem gì, sample bao nhiêu %, alert ở ngưỡng nào?
- Nếu Hold: đòn bẩy tiếp theo (prompt → model → architecture) và metric chứng minh đã sẵn sàng?

### Câu hỏi tự soi

- Tin cậy nhất ở đâu, đáng lo nhất ở đâu? (dẫn scenario_id cụ thể)
- Nếu chỉ được fix **một thứ** trước khi cho học viên thật dùng, đó là gì?
- Eval loop này sẽ chạy lại **khi nào** (mỗi lần đổi prompt? mỗi tuần? khi corpus đổi?) và ai nhìn kết quả?
- Điều gì trong bài này bạn sẽ **mang về áp dụng** vào sản phẩm thật của mình?
